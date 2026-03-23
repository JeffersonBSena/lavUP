"""
Data migration: cria o usuário administrador inicial a partir do .env.
"""
import os
from pathlib import Path
from django.db import migrations
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / '.env')


def seed_admin(apps, schema_editor):
    Usuario = apps.get_model('lavup', 'Usuario')

    nome = os.getenv('ADMIN_NOME', 'Administrador')
    email = os.getenv('ADMIN_EMAIL', 'admin@lavup.com.br')
    whatsapp = os.getenv('ADMIN_WHATSAPP', '')

    Usuario.objects.get_or_create(
        email=email,
        defaults={
            'nome': nome,
            'whatsapp': whatsapp,
            'tipo': 'admin',
            'ativo': True,
        },
    )


def reverse_admin(apps, schema_editor):
    email = os.getenv('ADMIN_EMAIL', 'admin@lavup.com.br')
    apps.get_model('lavup', 'Usuario').objects.filter(email=email).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('lavup', '0003_seed_fabricantes_tamanhos_veiculos'),
    ]

    operations = [
        migrations.RunPython(seed_admin, reverse_admin),
    ]
