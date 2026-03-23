import random
import string
from django.db import models
from django.utils import timezone
from django.conf import settings


class CodigoVerificacao(models.Model):
    usuario = models.ForeignKey(
        'lavup.Usuario',
        on_delete=models.CASCADE,
        related_name='codigos_verificacao',
        verbose_name='Usuário',
    )
    codigo = models.CharField(max_length=6, verbose_name='Código')
    tentativas = models.IntegerField(default=0, verbose_name='Tentativas')
    verificado = models.BooleanField(default=False, verbose_name='Verificado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    expires_at = models.DateTimeField(verbose_name='Expira em')

    class Meta:
        db_table = 'codigos_verificacao'
        verbose_name = 'Código de Verificação'
        verbose_name_plural = 'Códigos de Verificação'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.usuario} - {self.codigo}'

    def save(self, *args, **kwargs):
        if not self.codigo:
            length = getattr(settings, 'VERIFICATION_CODE_LENGTH', 6)
            self.codigo = ''.join(random.choices(string.digits, k=length))
        if not self.expires_at:
            minutes = getattr(settings, 'VERIFICATION_CODE_EXPIRY_MINUTES', 5)
            self.expires_at = timezone.now() + timezone.timedelta(minutes=minutes)
        super().save(*args, **kwargs)

    @property
    def expirado(self):
        return timezone.now() > self.expires_at

    @property
    def max_tentativas_excedido(self):
        max_attempts = getattr(settings, 'VERIFICATION_CODE_MAX_ATTEMPTS', 3)
        return self.tentativas >= max_attempts


class BloqueioLogin(models.Model):
    identificador = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Identificador',
        help_text='Email ou WhatsApp do usuário bloqueado',
    )
    tentativas_falhas = models.IntegerField(default=0, verbose_name='Tentativas Falhas')
    bloqueado_ate = models.DateTimeField(null=True, blank=True, verbose_name='Bloqueado até')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    TENTATIVAS_MAX = 5
    BLOQUEIO_MINUTOS = 30

    class Meta:
        db_table = 'bloqueios_login'
        verbose_name = 'Bloqueio de Login'
        verbose_name_plural = 'Bloqueios de Login'

    def __str__(self):
        return f'{self.identificador} - {self.tentativas_falhas} tentativas'

    @property
    def esta_bloqueado(self):
        if self.bloqueado_ate and timezone.now() < self.bloqueado_ate:
            return True
        return False

    @property
    def tempo_restante_bloqueio(self):
        if self.esta_bloqueado:
            delta = self.bloqueado_ate - timezone.now()
            return max(0, int(delta.total_seconds()))
        return 0

    def registrar_falha(self):
        self.tentativas_falhas += 1
        if self.tentativas_falhas >= self.TENTATIVAS_MAX:
            self.bloqueado_ate = timezone.now() + timezone.timedelta(
                minutes=self.BLOQUEIO_MINUTOS
            )
        self.save()

    def resetar(self):
        self.tentativas_falhas = 0
        self.bloqueado_ate = None
        self.save()
