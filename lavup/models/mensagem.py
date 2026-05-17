from django.db import models


class Mensagem(models.Model):
    slug = models.SlugField(max_length=64, unique=True, verbose_name='Slug')
    titulo = models.CharField(max_length=255, verbose_name='Título')
    corpo = models.TextField(verbose_name='Corpo')
    descricao = models.CharField(max_length=255, blank=True, verbose_name='Descrição')
    placeholders = models.CharField(
        max_length=255, blank=True,
        verbose_name='Placeholders',
        help_text='Lista separada por vírgula dos placeholders aceitos no corpo (ex.: codigo,minutos)',
    )
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        db_table = 'mensagens'
        verbose_name = 'Mensagem'
        verbose_name_plural = 'Mensagens'
        ordering = ['slug']

    def __str__(self):
        return self.titulo

    def render(self, **kwargs):
        """Renderiza o corpo substituindo placeholders no formato {nome}."""
        return self.corpo.format(**kwargs)
