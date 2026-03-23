import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from lavup.models import Tamanho


class Command(BaseCommand):
    help = 'Popula a tabela de tamanhos a partir do CSV'

    def handle(self, *args, **options):
        csv_path = Path(__file__).resolve().parents[3] / 'seeds' / 'tamanhos.csv'

        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            criados = 0
            for row in reader:
                _, created = Tamanho.objects.get_or_create(
                    nome=row['nome'],
                    defaults={
                        'incremento_valor': row['incremento_valor'],
                        'incremento_tempo': row['incremento_tempo'],
                    },
                )
                if created:
                    criados += 1

        self.stdout.write(self.style.SUCCESS(f'{criados} tamanhos criados.'))
