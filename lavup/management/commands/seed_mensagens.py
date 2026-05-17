import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from lavup.models import Mensagem


class Command(BaseCommand):
    help = 'Popula a tabela de mensagens (templates) a partir do CSV'

    def add_arguments(self, parser):
        parser.add_argument(
            '--update',
            action='store_true',
            help='Atualiza titulo/corpo/descricao/placeholders das mensagens já existentes',
        )

    def handle(self, *args, **options):
        csv_path = Path(__file__).resolve().parents[3] / 'seeds' / 'mensagens.csv'
        atualizar = options['update']

        criados = 0
        atualizados = 0
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                defaults = {
                    'titulo': row['titulo'],
                    'corpo': row['corpo'],
                    'descricao': row.get('descricao', ''),
                    'placeholders': row.get('placeholders', ''),
                }
                obj, created = Mensagem.objects.get_or_create(
                    slug=row['slug'], defaults=defaults
                )
                if created:
                    criados += 1
                elif atualizar:
                    for k, v in defaults.items():
                        setattr(obj, k, v)
                    obj.save()
                    atualizados += 1

        self.stdout.write(self.style.SUCCESS(
            f'{criados} mensagens criadas, {atualizados} atualizadas.'
        ))
