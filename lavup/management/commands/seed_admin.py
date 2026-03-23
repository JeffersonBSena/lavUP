import os
from django.core.management.base import BaseCommand
from lavup.models import Usuario


class Command(BaseCommand):
    help = 'Cria o usuário administrador inicial a partir do .env'

    def handle(self, *args, **options):
        nome = os.getenv('ADMIN_NOME')
        email = os.getenv('ADMIN_EMAIL')
        whatsapp = os.getenv('ADMIN_WHATSAPP')

        if not email:
            self.stdout.write(self.style.ERROR(
                'ADMIN_EMAIL não definido no .env. Seed cancelado.'
            ))
            return

        usuario, created = Usuario.objects.get_or_create(
            email=email,
            defaults={
                'nome': nome or 'Administrador',
                'whatsapp': whatsapp or '',
                'tipo': 'admin',
                'ativo': True,
            },
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Administrador criado: {usuario.nome} ({email})'))
        else:
            self.stdout.write(self.style.WARNING(f'Administrador já existe: {usuario.nome} ({email})'))
