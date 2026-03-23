from django.db import models


class Fabricante(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Nome')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        db_table = 'fabricantes'
        verbose_name = 'Fabricante'
        verbose_name_plural = 'Fabricantes'
        ordering = ['nome']

    def __str__(self):
        return self.nome
