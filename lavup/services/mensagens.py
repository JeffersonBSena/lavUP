import logging
from django.conf import settings
from lavup.models import Mensagem
from lavup.services.evolution_api import evolution_api

logger = logging.getLogger(__name__)


class MensagemService:
    """Despacha mensagens cujos templates ficam em ``Mensagem`` (tabela ``mensagens``).

    Use :py:meth:`enviar` com o ``slug`` do template e os placeholders necessários.
    Os wrappers ``enviar_*`` permanecem para compatibilidade com chamadas antigas.
    """

    @staticmethod
    def render(slug, **kwargs):
        """Carrega o template ativo pelo slug e renderiza substituindo placeholders."""
        try:
            msg = Mensagem.objects.get(slug=slug, ativo=True)
        except Mensagem.DoesNotExist:
            logger.error(f'[MensagemService] Template não encontrado: {slug}')
            raise
        try:
            return msg.render(**kwargs)
        except KeyError as e:
            logger.error(f'[MensagemService] Placeholder ausente em {slug}: {e}')
            raise

    @staticmethod
    def enviar(slug, phone, **kwargs):
        """Renderiza o template ``slug`` e envia ao ``phone`` via Evolution API."""
        texto = MensagemService.render(slug, **kwargs)
        return evolution_api.send_text(phone, texto)

    # ------------------------------------------------------------------
    # Wrappers de compatibilidade
    # ------------------------------------------------------------------

    @staticmethod
    def enviar_codigo_verificacao(phone, codigo):
        return MensagemService.enviar(
            'codigo_verificacao',
            phone,
            codigo=codigo,
            minutos=settings.VERIFICATION_CODE_EXPIRY_MINUTES,
        )

    @staticmethod
    def enviar_boas_vindas(phone, nome):
        return MensagemService.enviar('boas_vindas', phone, nome=nome)

    @staticmethod
    def enviar_os_criada(phone, numero_os, servicos):
        return MensagemService.enviar(
            'os_criada', phone, numero_os=numero_os, servicos=servicos,
        )

    @staticmethod
    def enviar_os_concluida(phone, numero_os):
        return MensagemService.enviar('os_concluida', phone, numero_os=numero_os)

    @staticmethod
    def enviar_agendamento_confirmado(phone, data, horario, servicos):
        return MensagemService.enviar(
            'agendamento_confirmado', phone,
            data=data, horario=horario, servicos=servicos,
        )

    @staticmethod
    def enviar_agendamento_cancelado(phone, data, horario):
        return MensagemService.enviar(
            'agendamento_cancelado', phone, data=data, horario=horario,
        )

    @staticmethod
    def enviar_lembrete_agendamento(phone, data, horario):
        return MensagemService.enviar(
            'lembrete_agendamento', phone, data=data, horario=horario,
        )
