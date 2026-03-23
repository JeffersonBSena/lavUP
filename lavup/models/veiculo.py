from django.db import models


class Veiculo(models.Model):
    fabricante = models.ForeignKey(
        'Fabricante',
        on_delete=models.CASCADE,
        related_name='veiculos',
        verbose_name='Fabricante',
        db_column='fabricantes_id',
    )
    tamanho = models.ForeignKey(
        'Tamanho',
        on_delete=models.CASCADE,
        related_name='veiculos',
        verbose_name='Tamanho',
        db_column='tamanhos_id',
    )
    modelo = models.CharField(max_length=255, verbose_name='Modelo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        db_table = 'veiculos'
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        ordering = ['modelo']

    def __str__(self):
        return f'{self.fabricante} {self.modelo}'
