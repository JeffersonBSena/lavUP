from django.db import models


class Agenda(models.Model):
    STATUS_CHOICES = [
        ('agendado', 'Agendado'),
        ('iniciado', 'Iniciado'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]

    os = models.OneToOneField(
        'OrdemServico',
        on_delete=models.CASCADE,
        related_name='agenda',
        verbose_name='Ordem de Serviço',
    )
    lavador = models.ForeignKey(
        'Usuario',
        on_delete=models.CASCADE,
        related_name='agendas',
        verbose_name='Lavador',
    )
    inicio_previsto = models.DateTimeField(verbose_name='Início Previsto')
    fim_previsto = models.DateTimeField(verbose_name='Fim Previsto')
    inicio_real = models.DateTimeField(null=True, blank=True, verbose_name='Início Real')
    fim_real = models.DateTimeField(null=True, blank=True, verbose_name='Fim Real')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='agendado', verbose_name='Status')
    motivo_cancelamento = models.TextField(null=True, blank=True, verbose_name='Motivo do Cancelamento')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        db_table = 'agenda'
        verbose_name = 'Agenda'
        verbose_name_plural = 'Agendas'
        ordering = ['-inicio_previsto']

    def __str__(self):
        return f'Agenda #{self.pk} - OS #{self.os_id} ({self.status})'
