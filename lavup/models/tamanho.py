from django.db import models


class Tamanho(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Nome')
    incremento_valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Incremento de Valor')
    incremento_tempo = models.IntegerField(verbose_name='Incremento de Tempo (min)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        db_table = 'tamanhos'
        verbose_name = 'Tamanho'
        verbose_name_plural = 'Tamanhos'
        ordering = ['nome']

    def __str__(self):
        return self.nome
