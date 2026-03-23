"""
Serviço de mensagens — monta o conteúdo e despacha via transporte (WhatsApp).

Para adicionar uma nova mensagem:
  1. Crie um método estático em MensagemTemplates que retorne o texto.
  2. Crie um método em MensagemService que chame o template e envie.

Exemplo:
    MensagemService.enviar_boas_vindas(phone, nome_cliente)
"""

import logging
from django.conf import settings
from lavup.services.evolution_api import evolution_api

logger = logging.getLogger(__name__)


class MensagemTemplates:
    """Templates de mensagens do sistema."""

    @staticmethod
    def codigo_verificacao(codigo):
        minutos = settings.VERIFICATION_CODE_EXPIRY_MINUTES
        return (
            f'*{settings.APP_NAME} - Código de Acesso*\n\n'
            f'Seu código de verificação é:\n\n'
            f'*{codigo}*\n\n'
            f'Este código expira em {minutos} minutos.\n'
            f'Se você não solicitou este código, ignore esta mensagem.'
        )

    @staticmethod
    def boas_vindas(nome):
        return (
            f'*{settings.APP_NAME} - Bem-vindo!*\n\n'
            f'Olá, {nome}! Seu cadastro foi realizado com sucesso.\n'
            f'Acesse o sistema para agendar seus serviços.'
        )

    @staticmethod
    def os_criada(numero_os, servicos):
        return (
            f'*{settings.APP_NAME} - Ordem de Serviço #{numero_os}*\n\n'
            f'Sua OS foi aberta com os seguintes serviços:\n'
            f'{servicos}\n\n'
            f'Acompanhe o status pelo sistema.'
        )

    @staticmethod
    def os_concluida(numero_os):
        return (
            f'*{settings.APP_NAME} - OS #{numero_os} Concluída*\n\n'
            f'Seu veículo está pronto! Pode retirá-lo quando quiser.\n'
            f'Obrigado pela preferência!'
        )

    @staticmethod
    def agendamento_confirmado(data, horario, servicos):
        return (
            f'*{settings.APP_NAME} - Agendamento Confirmado*\n\n'
            f'Data: {data}\n'
            f'Horário: {horario}\n'
            f'Serviços: {servicos}\n\n'
            f'Aguardamos você!'
        )

    @staticmethod
    def agendamento_cancelado(data, horario):
        return (
            f'*{settings.APP_NAME} - Agendamento Cancelado*\n\n'
            f'Seu agendamento de {data} às {horario} foi cancelado.\n'
            f'Para reagendar, acesse o sistema.'
        )

    @staticmethod
    def lembrete_agendamento(data, horario):
        return (
            f'*{settings.APP_NAME} - Lembrete*\n\n'
            f'Não esqueça do seu agendamento!\n'
            f'Data: {data}\n'
            f'Horário: {horario}\n\n'
            f'Aguardamos você!'
        )


class MensagemService:
    """Despacha mensagens formatadas via transporte configurado."""

    @staticmethod
    def enviar_codigo_verificacao(phone, codigo):
        texto = MensagemTemplates.codigo_verificacao(codigo)
        return evolution_api.send_text(phone, texto)

    @staticmethod
    def enviar_boas_vindas(phone, nome):
        texto = MensagemTemplates.boas_vindas(nome)
        return evolution_api.send_text(phone, texto)

    @staticmethod
    def enviar_os_criada(phone, numero_os, servicos):
        texto = MensagemTemplates.os_criada(numero_os, servicos)
        return evolution_api.send_text(phone, texto)

    @staticmethod
    def enviar_os_concluida(phone, numero_os):
        texto = MensagemTemplates.os_concluida(numero_os)
        return evolution_api.send_text(phone, texto)

    @staticmethod
    def enviar_agendamento_confirmado(phone, data, horario, servicos):
        texto = MensagemTemplates.agendamento_confirmado(data, horario, servicos)
        return evolution_api.send_text(phone, texto)

    @staticmethod
    def enviar_agendamento_cancelado(phone, data, horario):
        texto = MensagemTemplates.agendamento_cancelado(data, horario)
        return evolution_api.send_text(phone, texto)

    @staticmethod
    def enviar_lembrete_agendamento(phone, data, horario):
        texto = MensagemTemplates.lembrete_agendamento(data, horario)
        return evolution_api.send_text(phone, texto)
