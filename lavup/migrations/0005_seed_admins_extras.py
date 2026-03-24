"""
Data migration: cria usuários administradores adicionais.
"""
from django.db import migrations


ADMINS = [
    {
        'nome': 'José Vitor da Costa Lira',
        'email': '202502436815@alunos.estacio.br',
        'whatsapp': '5592992416087',
    },
    {
        'nome': 'Leonardo Maquiné de Oliveira',
        'email': '202303857047@alunos.estacio.br',
        'whatsapp': '5592999965762',
    },
    {
        'nome': 'Beatriz Cristina Gusmão da Mota',
        'email': '202502951914@alunos.estacio.br',
        'whatsapp': '5592992927634',
    },
]


def seed_admins(apps, schema_editor):
    Usuario = apps.get_model('lavup', 'Usuario')
    for admin in ADMINS:
        Usuario.objects.get_or_create(
            email=admin['email'],
            defaults={
                'nome': admin['nome'],
                'whatsapp': admin['whatsapp'],
                'tipo': 'admin',
                'ativo': True,
            },
        )


def reverse_admins(apps, schema_editor):
    Usuario = apps.get_model('lavup', 'Usuario')
    emails = [a['email'] for a in ADMINS]
    Usuario.objects.filter(email__in=emails).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('lavup', '0004_seed_admin'),
    ]

    operations = [
        migrations.RunPython(seed_admins, reverse_admins),
    ]
