import csv
from django.core.management.base import BaseCommand
from apps.loja.models import Produto

class Command(BaseCommand):
    help = 'Importa produtos do arquivo CSV'

    def handle(self, *args, **kwargs):
        with open('produtos_saucedemo_selenium.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader) 

            for row in reader:
                nome, preco = row
                Produto.objects.create(titulo=nome, preco=preco)
                self.stdout.write(self.style.SUCCESS(f'Produto "{nome}" importado com sucesso!'))

        self.stdout.write(self.style.SUCCESS('Importação concluída.'))
