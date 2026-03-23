from django.db import models


class Usuario(models.Model):
    TIPO_CHOICES = [
        ('admin', 'Administrador'),
        ('lavador', 'Lavador'),
    ]

    nome = models.CharField(max_length=255, verbose_name='Nome')
    email = models.CharField(max_length=255, unique=True, verbose_name='E-mail')
    whatsapp = models.CharField(max_length=20, null=True, blank=True, verbose_name='WhatsApp')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Excluído em')

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome} ({self.tipo})'
