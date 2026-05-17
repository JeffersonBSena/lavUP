from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from lavup.models import Agenda, Usuario
from lavup.services.mensagens import MensagemService
from lavup.views.crud import _notificar_agendamento


def _is_lavador(request):
    return request.session.get('lavup_usuario_tipo') == 'lavador'


def main(request):
    """Painel do lavador. Lavadores veem só as próprias agendas; admin/atendente vê tudo."""
    qs = (
        Agenda.objects
        .select_related('os', 'os__cliente', 'os__veiculo__fabricante', 'lavador')
        .prefetch_related('os__servicos__servico')
        .exclude(status__in=['concluido', 'cancelado'])
        .order_by('inicio_previsto')
    )
    if _is_lavador(request):
        qs = qs.filter(lavador_id=request.session.get('lavup_usuario_id'))

    return render(request, 'lavador.html', {
        'agendas': qs,
        'lavadores': Usuario.objects.filter(
            tipo='lavador', ativo=True, deleted_at__isnull=True
        ),
        'is_lavador': _is_lavador(request),
    })


def agenda_iniciar(request, pk):
    """Inicia o atendimento (status=iniciado, inicio_real=now, OS=iniciada)."""
    if request.method != 'POST':
        return redirect('lavador_main')
    agenda = get_object_or_404(Agenda, pk=pk)
    if agenda.status not in ('agendado',):
        messages.warning(request, f'Agenda já está "{agenda.get_status_display()}".')
        return redirect('lavador_main')
    agenda.status = 'iniciado'
    agenda.inicio_real = timezone.now()
    agenda.save(update_fields=['status', 'inicio_real', 'updated_at'])
    agenda.os.status = 'iniciada'
    agenda.os.save(update_fields=['status', 'updated_at'])
    messages.success(request, f'Atendimento iniciado (OS #{agenda.os_id}).')
    return redirect('lavador_main')


def agenda_reagendar(request, pk):
    """Reagenda. Recalcula fim_previsto pela soma dos tempos dos serviços."""
    if request.method != 'POST':
        return redirect('lavador_main')
    agenda = get_object_or_404(Agenda, pk=pk)
    if agenda.status in ('concluido', 'cancelado'):
        messages.warning(request, 'Agenda finalizada não pode ser reagendada.')
        return redirect('lavador_main')

    novo_inicio_str = request.POST.get('inicio_previsto', '').strip()
    novo_inicio = parse_datetime(novo_inicio_str)
    if not novo_inicio:
        messages.error(request, 'Data/hora inválida.')
        return redirect('lavador_main')
    if timezone.is_naive(novo_inicio):
        novo_inicio = timezone.make_aware(novo_inicio)

    tempo_total = sum(
        item.tempo_aplicado for item in agenda.os.servicos.all()
    ) or int((agenda.fim_previsto - agenda.inicio_previsto).total_seconds() // 60)

    status_anterior = agenda.status
    agenda.inicio_previsto = novo_inicio
    agenda.fim_previsto = novo_inicio + timedelta(minutes=tempo_total)
    agenda.status = 'agendado'
    agenda.inicio_real = None
    agenda.save()
    agenda.os.status = 'agendada'
    agenda.os.save(update_fields=['status', 'updated_at'])
    _notificar_agendamento(agenda, criado=False, status_anterior=status_anterior)
    messages.success(request, f'OS #{agenda.os_id} reagendada para {novo_inicio.strftime("%d/%m/%Y %H:%M")}.')
    return redirect('lavador_main')


def agenda_transferir(request, pk):
    """Transfere o atendimento para outro lavador."""
    if request.method != 'POST':
        return redirect('lavador_main')
    agenda = get_object_or_404(Agenda, pk=pk)
    novo_lavador_id = request.POST.get('lavador')
    if not novo_lavador_id:
        messages.error(request, 'Selecione um lavador.')
        return redirect('lavador_main')
    novo = get_object_or_404(Usuario, pk=novo_lavador_id, tipo='lavador', ativo=True)
    if novo.id == agenda.lavador_id:
        messages.warning(request, 'Lavador é o mesmo já atribuído.')
        return redirect('lavador_main')
    anterior = agenda.lavador.nome
    agenda.lavador = novo
    agenda.save(update_fields=['lavador', 'updated_at'])
    messages.success(request, f'OS #{agenda.os_id} transferida de {anterior} para {novo.nome}.')
    return redirect('lavador_main')


def agenda_concluir(request, pk):
    """Encerra o atendimento. Grava observações na OS e dispara WhatsApp 'os_concluida'."""
    if request.method != 'POST':
        return redirect('lavador_main')
    agenda = get_object_or_404(Agenda, pk=pk)
    if agenda.status != 'iniciado':
        messages.warning(request, f'Só é possível concluir agendas iniciadas (status atual: {agenda.get_status_display()}).')
        return redirect('lavador_main')

    obs = request.POST.get('observacoes', '').strip()

    agenda.status = 'concluido'
    agenda.fim_real = timezone.now()
    agenda.save(update_fields=['status', 'fim_real', 'updated_at'])

    if obs:
        prev = agenda.os.observacoes or ''
        agenda.os.observacoes = (prev + '\n' if prev else '') + f'[Fechamento] {obs}'
    agenda.os.status = 'concluida'
    agenda.os.save(update_fields=['status', 'observacoes', 'updated_at'])

    phone = agenda.os.cliente.whatsapp if agenda.os.cliente else None
    if phone:
        MensagemService.enviar_os_concluida(phone, agenda.os_id)

    messages.success(request, f'OS #{agenda.os_id} concluída. Cliente notificado.')
    return redirect('lavador_main')


def agenda_cancelar(request, pk):
    """Cancela informando o motivo (texto obrigatório)."""
    if request.method != 'POST':
        return redirect('lavador_main')
    agenda = get_object_or_404(Agenda, pk=pk)
    motivo = request.POST.get('motivo', '').strip()
    if not motivo:
        messages.error(request, 'Informe o motivo do cancelamento.')
        return redirect('lavador_main')
    status_anterior = agenda.status
    agenda.status = 'cancelado'
    agenda.motivo_cancelamento = motivo
    agenda.save(update_fields=['status', 'motivo_cancelamento', 'updated_at'])
    agenda.os.status = 'cancelada'
    agenda.os.save(update_fields=['status', 'updated_at'])
    _notificar_agendamento(agenda, criado=False, status_anterior=status_anterior)
    messages.success(request, f'OS #{agenda.os_id} cancelada.')
    return redirect('lavador_main')
