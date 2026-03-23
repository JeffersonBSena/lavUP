"""
Data migration: popula fabricantes, tamanhos e veículos a partir dos CSVs.
"""
import csv
from pathlib import Path
from django.db import migrations


BASE_DIR = Path(__file__).resolve().parents[2]


def carregar_csv(nome_arquivo):
    csv_path = BASE_DIR / 'seeds' / nome_arquivo
    with open(csv_path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def seed_fabricantes(apps, schema_editor):
    Fabricante = apps.get_model('lavup', 'Fabricante')
    for row in carregar_csv('fabricantes.csv'):
        Fabricante.objects.get_or_create(nome=row['nome'])


def seed_tamanhos(apps, schema_editor):
    Tamanho = apps.get_model('lavup', 'Tamanho')
    for row in carregar_csv('tamanhos.csv'):
        Tamanho.objects.get_or_create(
            nome=row['nome'],
            defaults={
                'incremento_valor': row['incremento_valor'],
                'incremento_tempo': row['incremento_tempo'],
            },
        )


def seed_veiculos(apps, schema_editor):
    Fabricante = apps.get_model('lavup', 'Fabricante')
    Tamanho = apps.get_model('lavup', 'Tamanho')
    Veiculo = apps.get_model('lavup', 'Veiculo')
    for row in carregar_csv('veiculos.csv'):
        fabricante = Fabricante.objects.get(nome=row['fabricante'])
        tamanho = Tamanho.objects.get(nome=row['tamanho'])
        Veiculo.objects.get_or_create(
            fabricante=fabricante,
            modelo=row['modelo'],
            defaults={'tamanho': tamanho},
        )


def reverse_all(apps, schema_editor):
    """Remove todos os dados seedados (rollback)."""
    apps.get_model('lavup', 'Veiculo').objects.all().delete()
    apps.get_model('lavup', 'Tamanho').objects.all().delete()
    apps.get_model('lavup', 'Fabricante').objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('lavup', '0002_bloqueiologin_codigoverificacao'),
    ]

    operations = [
        migrations.RunPython(seed_fabricantes, reverse_all),
        migrations.RunPython(seed_tamanhos, migrations.RunPython.noop),
        migrations.RunPython(seed_veiculos, migrations.RunPython.noop),
    ]
