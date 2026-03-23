from django.db import models


class Servico(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Nome')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    descricao = models.TextField(null=True, blank=True, verbose_name='Descrição')
    valor_base = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor Base')
    incremento_tempo = models.IntegerField(verbose_name='Incremento de Tempo (min)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        db_table = 'servicos'
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
        ordering = ['nome']

    def __str__(self):
        return self.nome
