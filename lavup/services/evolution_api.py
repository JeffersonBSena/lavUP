import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class EvolutionAPI:
    """Cliente de transporte — envia mensagens via Evolution API (WhatsApp)."""

    def __init__(self):
        self.base_url = settings.EVOLUTION_API_URL
        self.token = settings.EVOLUTION_API_TOKEN
        self.instance = settings.EVOLUTION_INSTANCE
        self.enabled = settings.EVOLUTION_ENABLED

    @property
    def headers(self):
        return {
            'Content-Type': 'application/json',
            'apikey': self.token,
        }

    def _format_phone(self, phone):
        """Remove caracteres não numéricos e garante formato com DDI."""
        digits = ''.join(filter(str.isdigit, phone))
        if not digits.startswith('55'):
            digits = '55' + digits
        return digits

    def send_text(self, phone, message):
        """Envia mensagem de texto para um número WhatsApp."""
        if not self.enabled:
            logger.warning(f'[EvolutionAPI] Desabilitada. Mensagem para {phone}: {message}')
            return {'status': 'disabled', 'message': message}

        url = f'{self.base_url}/message/sendText/{self.instance}'
        payload = {
            'number': self._format_phone(phone),
            'text': message,
        }

        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            response.raise_for_status()
            logger.info(f'[EvolutionAPI] Mensagem enviada para {phone}')
            return response.json()
        except requests.RequestException as e:
            logger.error(f'[EvolutionAPI] Erro ao enviar para {phone}: {e}')
            return {'status': 'error', 'detail': str(e)}


evolution_api = EvolutionAPI()
