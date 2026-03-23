import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from lavup.models import Fabricante


class Command(BaseCommand):
    help = 'Popula a tabela de fabricantes a partir do CSV'

    def handle(self, *args, **options):
        csv_path = Path(__file__).resolve().parents[3] / 'seeds' / 'fabricantes.csv'

        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            criados = 0
            for row in reader:
                _, created = Fabricante.objects.get_or_create(nome=row['nome'])
                if created:
                    criados += 1

        self.stdout.write(self.style.SUCCESS(f'{criados} fabricantes criados.'))
