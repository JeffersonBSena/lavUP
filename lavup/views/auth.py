import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone

from lavup.models import Usuario, CodigoVerificacao, BloqueioLogin
from lavup.services.mensagens import MensagemService

logger = logging.getLogger(__name__)


def login_identify(request):
    """Etapa 1: Usuário informa email ou WhatsApp."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        identificador = request.POST.get('identificador', '').strip()

        if not identificador:
            messages.error(request, 'Informe seu e-mail ou WhatsApp.')
            return render(request, 'auth/login_identify.html')

        # Verificar bloqueio
        bloqueio, _ = BloqueioLogin.objects.get_or_create(identificador=identificador)
        if bloqueio.esta_bloqueado:
            minutos = bloqueio.tempo_restante_bloqueio // 60
            segundos = bloqueio.tempo_restante_bloqueio % 60
            messages.error(
                request,
                f'Acesso bloqueado. Tente novamente em {minutos}min {segundos}s.'
            )
            return render(request, 'auth/login_identify.html', {
                'identificador': identificador,
                'bloqueado': True,
                'tempo_restante': bloqueio.tempo_restante_bloqueio,
            })

        # Buscar usuário por email ou whatsapp
        digits = ''.join(filter(str.isdigit, identificador))
        usuario = Usuario.objects.filter(
            Q(email__iexact=identificador) | Q(whatsapp=digits if digits else None),
            ativo=True,
            deleted_at__isnull=True,
        ).first()

        if not usuario:
            bloqueio.registrar_falha()
            tentativas_restantes = BloqueioLogin.TENTATIVAS_MAX - bloqueio.tentativas_falhas
            if bloqueio.esta_bloqueado:
                messages.error(
                    request,
                    f'Usuário não encontrado. Acesso bloqueado por {BloqueioLogin.BLOQUEIO_MINUTOS} minutos.'
                )
            elif tentativas_restantes <= 2:
                messages.warning(
                    request,
                    f'Usuário não encontrado. Restam {tentativas_restantes} tentativa(s) antes do bloqueio.'
                )
            else:
                messages.error(request, 'Usuário não encontrado.')
            return render(request, 'auth/login_identify.html', {
                'identificador': identificador,
            })

        # Invalidar códigos anteriores não utilizados
        CodigoVerificacao.objects.filter(
            usuario=usuario, verificado=False
        ).delete()

        # Gerar e enviar novo código
        codigo = CodigoVerificacao(usuario=usuario)
        codigo.save()

        # Enviar via WhatsApp se o usuário tiver número
        if usuario.whatsapp:
            result = MensagemService.enviar_codigo_verificacao(usuario.whatsapp, codigo.codigo)
            logger.info(f'Código enviado para {usuario.whatsapp}: {result}')
            destino = _mask_phone(usuario.whatsapp)
            messages.success(request, f'Código enviado para WhatsApp {destino}')
        else:
            # Fallback: mostrar no console (dev only)
            logger.warning(f'[DEV] Código para {usuario.email}: {codigo.codigo}')
            messages.info(request, 'Código de verificação enviado.')

        # Salvar dados na sessão
        request.session['auth_usuario_id'] = usuario.id
        request.session['auth_codigo_id'] = codigo.id
        request.session['auth_identificador'] = identificador

        return redirect('login_verify')

    return render(request, 'auth/login_identify.html')


def login_verify(request):
    """Etapa 2: Usuário informa o código de 6 dígitos."""
    usuario_id = request.session.get('auth_usuario_id')
    codigo_id = request.session.get('auth_codigo_id')
    identificador = request.session.get('auth_identificador', '')

    if not usuario_id or not codigo_id:
        return redirect('login')

    try:
        codigo = CodigoVerificacao.objects.get(id=codigo_id, usuario_id=usuario_id)
        usuario = codigo.usuario
    except CodigoVerificacao.DoesNotExist:
        messages.error(request, 'Sessão expirada. Tente novamente.')
        return redirect('login')

    if request.method == 'POST':
        codigo_informado = request.POST.get('codigo', '').strip()

        # Verificar expiração
        if codigo.expirado:
            messages.error(request, 'Código expirado. Solicite um novo código.')
            _limpar_sessao_auth(request)
            return redirect('login')

        # Verificar tentativas do código
        if codigo.max_tentativas_excedido:
            messages.error(request, 'Número máximo de tentativas excedido. Solicite novo código.')
            _limpar_sessao_auth(request)
            return redirect('login')

        # Validar código
        if codigo_informado == codigo.codigo:
            codigo.verificado = True
            codigo.save()

            # Resetar bloqueio
            BloqueioLogin.objects.filter(identificador=identificador).update(
                tentativas_falhas=0, bloqueado_ate=None
            )

            # Criar/buscar Django User e autenticar
            django_user, _ = User.objects.get_or_create(
                username=f'usuario_{usuario.id}',
                defaults={
                    'email': usuario.email,
                    'first_name': usuario.nome.split()[0] if usuario.nome else '',
                    'last_name': ' '.join(usuario.nome.split()[1:]) if usuario.nome else '',
                },
            )
            auth_login(request, django_user)

            # Guardar dados do usuário LavUP na sessão
            request.session['lavup_usuario_id'] = usuario.id
            request.session['lavup_usuario_nome'] = usuario.nome
            request.session['lavup_usuario_tipo'] = usuario.tipo

            _limpar_sessao_auth(request)
            messages.success(request, f'Bem-vindo, {usuario.nome}!')
            return redirect('dashboard')
        else:
            codigo.tentativas += 1
            codigo.save()
            restantes = (
                getattr(codigo, '_meta').model.objects.get(pk=codigo.pk)
            )
            tentativas_max = 3
            tentativas_restantes = tentativas_max - codigo.tentativas
            if tentativas_restantes > 0:
                messages.error(
                    request,
                    f'Código incorreto. Restam {tentativas_restantes} tentativa(s).'
                )
            else:
                messages.error(request, 'Número máximo de tentativas excedido.')
                _limpar_sessao_auth(request)
                return redirect('login')

    # Calcular tempo restante para expiração
    tempo_restante = max(0, int((codigo.expires_at - timezone.now()).total_seconds()))

    return render(request, 'auth/login_verify.html', {
        'tempo_restante': tempo_restante,
        'whatsapp_masked': _mask_phone(usuario.whatsapp) if usuario.whatsapp else None,
    })


def logout_view(request):
    """Logout do usuário."""
    auth_logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('login')


def dashboard(request):
    """Página inicial após login."""
    from lavup.models.veiculo import Veiculo
    context = {
        'veiculos_total': Veiculo.objects.count(),
    }
    return render(request, 'dashboard.html', context)


# --- Helpers ---

def _mask_phone(phone):
    """Mascara número de telefone: (11) ****-1234"""
    digits = ''.join(filter(str.isdigit, phone))
    if len(digits) >= 4:
        return f'****-{digits[-4:]}'
    return '****'


def _limpar_sessao_auth(request):
    """Remove dados temporários de autenticação da sessão."""
    for key in ['auth_usuario_id', 'auth_codigo_id', 'auth_identificador']:
        request.session.pop(key, None)
