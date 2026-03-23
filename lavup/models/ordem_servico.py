from django.db import models


class OrdemServico(models.Model):
    STATUS_CHOICES = [
        ('aberta', 'Aberta'),
        ('iniciada', 'Iniciada'),
        ('agendada', 'Agendada'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]

    cliente = models.ForeignKey(
        'Cliente',
        on_delete=models.CASCADE,
        related_name='ordens_servico',
        verbose_name='Cliente',
    )
    veiculo = models.ForeignKey(
        'Veiculo',
        on_delete=models.CASCADE,
        related_name='ordens_servico',
        verbose_name='Veículo',
        db_column='veiculos_id',
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberta', verbose_name='Status')
    observacoes = models.TextField(null=True, blank=True, verbose_name='Observações')
    placa_veiculo = models.CharField(max_length=20, verbose_name='Placa do Veículo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        db_table = 'ordem_servico'
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'
        ordering = ['-created_at']

    def __str__(self):
        return f'OS #{self.pk} - {self.cliente} ({self.status})'


class OrdemServicoServico(models.Model):
    ordem_servico = models.ForeignKey(
        OrdemServico,
        on_delete=models.CASCADE,
        related_name='servicos',
        verbose_name='Ordem de Serviço',
        db_column='os_id',
    )
    servico = models.ForeignKey(
        'Servico',
        on_delete=models.CASCADE,
        related_name='ordens_servico',
        verbose_name='Serviço',
    )
    valor_aplicado = models.CharField(max_length=20, verbose_name='Valor Aplicado')
    tempo_aplicado = models.IntegerField(verbose_name='Tempo Aplicado (min)')

    class Meta:
        db_table = 'os_servicos'
        verbose_name = 'Serviço da OS'
        verbose_name_plural = 'Serviços da OS'
        unique_together = ['ordem_servico', 'servico']

    def __str__(self):
        return f'OS #{self.ordem_servico_id} - {self.servico}'
