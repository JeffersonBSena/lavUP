from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from lavup.models import (
    Fabricante, Tamanho, Veiculo,
    Cliente, Servico, Usuario,
    OrdemServico, OrdemServicoServico, Agenda,
)
from lavup.services.mensagens import MensagemService


# ============================================================
# AGENDA  (relação 1:1 com OrdemServico)
# ============================================================

def agenda(request):
    """Lista os agendamentos com OS, cliente e lavador relacionados."""
    context = {
        'agendamentos': (
            Agenda.objects
            .select_related('os', 'os__cliente', 'lavador')
            .all()
        ),
        # OS sem agenda ainda — para o select do form
        'ordens': (
            OrdemServico.objects
            .filter(agenda__isnull=True)
            .select_related('cliente')
        ),
        'usuarios': Usuario.objects.filter(tipo='lavador', ativo=True, deleted_at__isnull=True),
    }
    return render(request, 'agenda.html', context)


def agenda_criar(request):
    """Cria um novo agendamento (OS:Agenda 1:1)."""
    if request.method == 'POST':
        try:
            os_obj = get_object_or_404(OrdemServico, pk=request.POST['os'])
            agenda_obj, created = Agenda.objects.update_or_create(
                os=os_obj,
                defaults={
                    'lavador_id': request.POST['lavador'],
                    'inicio_previsto': request.POST['inicio_previsto'],
                    'fim_previsto': request.POST['fim_previsto'],
                    'status': request.POST.get('status', 'agendado'),
                    'motivo_cancelamento': request.POST.get('motivo_cancelamento') or None,
                },
            )
            _notificar_agendamento(agenda_obj, criado=created)
            messages.success(request, 'Agendamento salvo.' if created else 'Agendamento atualizado.')
        except (KeyError, IntegrityError) as e:
            messages.error(request, f'Erro ao salvar agendamento: {e}')
    return redirect('agenda')


def agenda_editar(request, pk):
    """Edita um agendamento existente (reagendamento via UPDATE)."""
    agenda_obj = get_object_or_404(Agenda, pk=pk)
    if request.method == 'POST':
        status_anterior = agenda_obj.status
        agenda_obj.lavador_id = request.POST.get('lavador', agenda_obj.lavador_id)
        agenda_obj.inicio_previsto = request.POST.get('inicio_previsto', agenda_obj.inicio_previsto)
        agenda_obj.fim_previsto = request.POST.get('fim_previsto', agenda_obj.fim_previsto)
        agenda_obj.status = request.POST.get('status', agenda_obj.status)
        agenda_obj.motivo_cancelamento = request.POST.get('motivo_cancelamento') or None

        if agenda_obj.status == 'iniciado' and not agenda_obj.inicio_real:
            agenda_obj.inicio_real = timezone.now()
        if agenda_obj.status == 'concluido' and not agenda_obj.fim_real:
            agenda_obj.fim_real = timezone.now()

        agenda_obj.save()
        _notificar_agendamento(agenda_obj, criado=False, status_anterior=status_anterior)
        messages.success(request, 'Agendamento atualizado.')
    return redirect('agenda')


def agenda_deletar(request, pk):
    agenda_obj = get_object_or_404(Agenda, pk=pk)
    if request.method == 'POST':
        agenda_obj.delete()
        messages.success(request, 'Agendamento removido.')
    return redirect('agenda')


def _notificar_agendamento(agenda_obj, criado, status_anterior=None):
    """Envia WhatsApp ao cliente conforme status da agenda."""
    cliente = agenda_obj.os.cliente
    phone = cliente.whatsapp if cliente else None
    if not phone:
        return

    data = agenda_obj.inicio_previsto.strftime('%d/%m/%Y')
    horario = agenda_obj.inicio_previsto.strftime('%H:%M')

    if agenda_obj.status == 'cancelado' and status_anterior != 'cancelado':
        MensagemService.enviar_agendamento_cancelado(phone, data, horario)
    elif agenda_obj.status == 'agendado':
        servicos = ', '.join(
            s.servico.nome for s in agenda_obj.os.servicos.select_related('servico').all()
        ) or 'A confirmar'
        MensagemService.enviar_agendamento_confirmado(phone, data, horario, servicos)


# ============================================================
# CLIENTES
# ============================================================

def clientes(request):
    return render(request, 'clientes.html', {
        'clientes': Cliente.objects.all(),
    })


def cliente_criar(request):
    if request.method == 'POST':
        cliente = Cliente.objects.create(
            nome=request.POST['nome'],
            whatsapp=request.POST.get('whatsapp') or None,
        )
        messages.success(request, 'Cliente cadastrado.')
        if cliente.whatsapp:
            MensagemService.enviar_boas_vindas(cliente.whatsapp, cliente.nome)
    return redirect('clientes')


def cliente_editar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.nome = request.POST.get('nome', cliente.nome)
        cliente.whatsapp = request.POST.get('whatsapp') or None
        cliente.save()
        messages.success(request, 'Cliente atualizado.')
    return redirect('clientes')


def cliente_deletar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        try:
            cliente.delete()
            messages.success(request, 'Cliente removido.')
        except IntegrityError:
            messages.error(request, 'Não é possível remover: cliente possui Ordens de Serviço.')
    return redirect('clientes')


# ============================================================
# VEÍCULOS
# ============================================================

def veiculos(request):
    return render(request, 'veiculos.html', {
        'veiculos': Veiculo.objects.select_related('fabricante', 'tamanho').all(),
        'fabricantes': Fabricante.objects.all(),
        'tamanhos': Tamanho.objects.all(),
    })


def veiculo_criar(request):
    if request.method == 'POST':
        Veiculo.objects.create(
            fabricante_id=request.POST['fabricante'],
            modelo=request.POST['modelo'],
            tamanho_id=request.POST['tamanho'],
        )
    return redirect('veiculos')


def veiculo_editar(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    if request.method == 'POST':
        veiculo.fabricante_id = request.POST['fabricante']
        veiculo.modelo = request.POST['modelo']
        veiculo.tamanho_id = request.POST['tamanho']
        veiculo.save()
    return redirect('veiculos')


def veiculo_deletar(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    if request.method == 'POST':
        veiculo.delete()
    return redirect('veiculos')


# ============================================================
# SERVIÇOS
# ============================================================

def servicos(request):
    return render(request, 'servicos.html', {
        'servicos': Servico.objects.all(),
    })


def servico_criar(request):
    if request.method == 'POST':
        Servico.objects.create(
            nome=request.POST['nome'],
            descricao=request.POST.get('descricao') or None,
            valor_base=request.POST['valor_base'],
            incremento_tempo=request.POST['incremento_tempo'],
            ativo='ativo' in request.POST,
        )
        messages.success(request, 'Serviço cadastrado.')
    return redirect('servicos')


def servico_editar(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        servico.nome = request.POST.get('nome', servico.nome)
        servico.descricao = request.POST.get('descricao') or None
        servico.valor_base = request.POST.get('valor_base', servico.valor_base)
        servico.incremento_tempo = request.POST.get('incremento_tempo', servico.incremento_tempo)
        servico.ativo = 'ativo' in request.POST
        servico.save()
        messages.success(request, 'Serviço atualizado.')
    return redirect('servicos')


def servico_deletar(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        try:
            servico.delete()
            messages.success(request, 'Serviço removido.')
        except IntegrityError:
            messages.error(request, 'Serviço em uso por OS — desative em vez de excluir.')
    return redirect('servicos')


# ============================================================
# USUÁRIOS  (admin / lavador) — soft delete via deleted_at
# ============================================================

def usuarios(request):
    return render(request, 'usuarios.html', {
        'usuarios': Usuario.objects.filter(deleted_at__isnull=True),
    })


def usuario_criar(request):
    if request.method == 'POST':
        try:
            usuario = Usuario.objects.create(
                nome=request.POST['nome'],
                email=request.POST['email'],
                whatsapp=request.POST.get('whatsapp') or None,
                tipo=request.POST['tipo'],
                ativo=True,
            )
            messages.success(request, f'Usuário "{usuario.nome}" cadastrado.')
        except IntegrityError:
            messages.error(request, 'E-mail já cadastrado.')
    return redirect('usuarios')


def usuario_editar(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk, deleted_at__isnull=True)
    if request.method == 'POST':
        usuario.nome = request.POST.get('nome', usuario.nome)
        usuario.email = request.POST.get('email', usuario.email)
        usuario.whatsapp = request.POST.get('whatsapp') or None
        usuario.tipo = request.POST.get('tipo', usuario.tipo)
        try:
            usuario.save()
            messages.success(request, 'Usuário atualizado.')
        except IntegrityError:
            messages.error(request, 'E-mail já em uso por outro usuário.')
    return redirect('usuarios')


def usuario_deletar(request, pk):
    """Soft delete — preserva histórico via deleted_at."""
    usuario = get_object_or_404(Usuario, pk=pk, deleted_at__isnull=True)
    if request.method == 'POST':
        usuario.deleted_at = timezone.now()
        usuario.ativo = False
        usuario.save(update_fields=['deleted_at', 'ativo', 'updated_at'])
        messages.success(request, 'Usuário removido.')
    return redirect('usuarios')


# ============================================================
# ORDENS DE SERVIÇO  (com criação simultânea de Agenda)
# ============================================================

def ordens(request):
    """Lista as OS com cliente, veículo e agenda associada."""
    return render(request, 'os.html', {
        'ordens': (
            OrdemServico.objects
            .select_related('cliente', 'veiculo', 'veiculo__fabricante', 'agenda', 'agenda__lavador')
            .prefetch_related('servicos__servico')
            .all()
        ),
        'clientes': Cliente.objects.all(),
        'veiculos': Veiculo.objects.select_related('fabricante').all(),
        'servicos_disponiveis': Servico.objects.filter(ativo=True),
        'lavadores': Usuario.objects.filter(tipo='lavador', ativo=True, deleted_at__isnull=True),
    })


def os_criar(request):
    """Cria uma OS + itens (N:N) + Agenda (1:1).

    ``tipo=fila`` força inicio_previsto=now (cliente está no local agora).
    ``tipo=agendamento`` usa inicio_previsto informado.
    fim_previsto = inicio + soma dos tempos dos serviços.
    """
    if request.method == 'POST':
        try:
            with transaction.atomic():
                cliente = get_object_or_404(Cliente, pk=request.POST['cliente'])
                veiculo = get_object_or_404(Veiculo, pk=request.POST['veiculo'])
                lavador_id = request.POST.get('lavador') or None
                tipo = request.POST.get('tipo', 'agendamento')
                servico_ids = request.POST.getlist('servicos')

                if not servico_ids:
                    messages.error(request, 'Selecione ao menos um serviço.')
                    return redirect('ordens')
                if not lavador_id:
                    messages.error(request, 'Selecione um lavador.')
                    return redirect('ordens')

                os_obj = OrdemServico.objects.create(
                    cliente=cliente,
                    veiculo=veiculo,
                    placa_veiculo=request.POST.get('placa_veiculo', '').strip(),
                    observacoes=request.POST.get('observacoes') or None,
                    status='agendada',
                )

                # Itens (N:N) com snapshot de valor/tempo
                tempo_total = 0
                for sid in servico_ids:
                    s = Servico.objects.get(pk=sid)
                    OrdemServicoServico.objects.create(
                        ordem_servico=os_obj,
                        servico=s,
                        valor_aplicado=s.valor_base,
                        tempo_aplicado=s.incremento_tempo,
                    )
                    tempo_total += s.incremento_tempo

                # Agenda 1:1
                if tipo == 'fila':
                    inicio = timezone.now()
                else:
                    inicio = parse_datetime(request.POST['inicio_previsto'])
                    if inicio and timezone.is_naive(inicio):
                        inicio = timezone.make_aware(inicio)

                fim = inicio + timedelta(minutes=tempo_total)

                agenda_obj = Agenda.objects.create(
                    os=os_obj,
                    lavador_id=lavador_id,
                    inicio_previsto=inicio,
                    fim_previsto=fim,
                    status='agendado',
                    inicio_real=None,
                )
                _notificar_agendamento(agenda_obj, criado=True)

                rotulo = 'na fila (cliente no local)' if tipo == 'fila' else 'agendada'
                messages.success(
                    request,
                    f'OS #{os_obj.id} {rotulo}. Aguardando Iniciar no Painel do Lavador. Tempo previsto: {tempo_total} min.'
                )
        except (KeyError, IntegrityError, ValueError) as e:
            messages.error(request, f'Erro ao criar OS: {e}')
    return redirect('ordens')


def os_editar(request, pk):
    """Atualiza dados básicos da OS (sem mexer em itens nem agenda).

    Regra: OS em estado terminal (concluida/cancelada) é histórica e não pode
    ser reaberta nem ter dados alterados via edição comum.
    """
    os_obj = get_object_or_404(OrdemServico, pk=pk)
    if request.method == 'POST':
        if os_obj.status in ('concluida', 'cancelada'):
            messages.warning(
                request,
                f'OS #{os_obj.id} está {os_obj.get_status_display().lower()} e não pode ser editada.'
            )
            return redirect('ordens')

        novo_status = request.POST.get('status', os_obj.status)
        # Não permite forçar a OS para estado terminal por aqui (use Concluir/Cancelar no Painel do Lavador).
        if novo_status in ('concluida', 'cancelada') and novo_status != os_obj.status:
            messages.warning(
                request,
                'Para concluir ou cancelar, utilize o Painel do Lavador (registra observações/motivo e notifica o cliente).'
            )
            return redirect('ordens')

        os_obj.cliente_id = request.POST.get('cliente', os_obj.cliente_id)
        os_obj.veiculo_id = request.POST.get('veiculo', os_obj.veiculo_id)
        os_obj.placa_veiculo = request.POST.get('placa_veiculo', os_obj.placa_veiculo).strip()
        os_obj.observacoes = request.POST.get('observacoes') or None
        os_obj.status = novo_status
        os_obj.save()
        messages.success(request, f'OS #{os_obj.id} atualizada.')
    return redirect('ordens')


def os_deletar(request, pk):
    os_obj = get_object_or_404(OrdemServico, pk=pk)
    if request.method == 'POST':
        os_obj.delete()
        messages.success(request, 'OS removida.')
    return redirect('ordens')


# ============================================================
# CONFIGURAÇÕES
# ============================================================

def configuracoes(request):
    return render(request, 'configuracoes.html')
