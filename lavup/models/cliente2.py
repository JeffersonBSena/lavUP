from django.db import models


class Cliente2(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Nome')
    whatsapp = models.CharField(max_length=20, null=True, blank=True, verbose_name='WhatsApp')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        db_table = 'clientes2'
        verbose_name = 'Cliente2'
        verbose_name_plural = 'Clientes2'
        ordering = ['nome']

    def __str__(self):
        return self.nome
