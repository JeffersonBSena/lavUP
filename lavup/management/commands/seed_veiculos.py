import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from lavup.models import Fabricante, Tamanho, Veiculo


class Command(BaseCommand):
    help = 'Popula a tabela de veículos a partir do CSV'

    def handle(self, *args, **options):
        csv_path = Path(__file__).resolve().parents[3] / 'seeds' / 'veiculos.csv'

        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            criados = 0
            for row in reader:
                fabricante = Fabricante.objects.get(nome=row['fabricante'])
                tamanho = Tamanho.objects.get(nome=row['tamanho'])

                _, created = Veiculo.objects.get_or_create(
                    fabricante=fabricante,
                    modelo=row['modelo'],
                    defaults={'tamanho': tamanho},
                )
                if created:
                    criados += 1

        self.stdout.write(self.style.SUCCESS(f'{criados} veículos criados.'))
