# produtos/management/commands/import_products.py

import csv
import re
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand, CommandError
from produtos.models import Product

class Command(BaseCommand):
    help = 'Importa produtos a partir de um arquivo CSV.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Caminho para o arquivo CSV.')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        self.stdout.write(f'Iniciando a importação do arquivo: {csv_file}')

        try:
            with open(csv_file, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                expected_headers = ['Nome do Produto', 'Descrição', 'Preço']
                if reader.fieldnames != expected_headers:
                    self.stdout.write(self.style.ERROR(f'Cabeçalhos do CSV incorretos. Esperado: {expected_headers}'))
                    raise CommandError('Cabeçalhos do CSV inválidos.')

                count = 0
                for row in reader:
                    product_name = row.get('Nome do Produto')
                    description = row.get('Descrição')
                    price = row.get('Preço')

                    if not product_name or not description or not price:
                        self.stdout.write(self.style.WARNING(f"Linha incompleta: {row}"))
                        continue

                    # Remover símbolos de moeda e espaços
                    price_cleaned = re.sub(r'[^\d.,-]', '', price)

                    # Substituir vírgulas por pontos, se necessário
                    price_cleaned = price_cleaned.replace(',', '.')

                    try:
                        price_decimal = Decimal(price_cleaned)
                    except InvalidOperation:
                        self.stdout.write(self.style.WARNING(f"Preço inválido para o produto '{product_name}': {price}"))
                        continue

                    product, created = Product.objects.get_or_create(
                        name=product_name,
                        defaults={
                            'description': description,
                            'price': price_decimal
                        }
                    )
                    if not created:
                        # Atualizar o produto existente
                        product.description = description
                        product.price = price_decimal
                        product.save()
                        self.stdout.write(self.style.NOTICE(f"Produto atualizado: {product_name}"))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"Produto criado: {product_name}"))
                    count += 1

            self.stdout.write(self.style.SUCCESS(f'Importação concluída. {count} produtos importados ou atualizados.'))
        except FileNotFoundError:
            raise CommandError(f'Arquivo "{csv_file}" não encontrado.')
        except KeyError as e:
            raise CommandError(f'Cabeçalho do CSV inválido ou faltando: {e}')
        except Exception as e:
            raise CommandError(f'Ocorreu um erro: {e}')
