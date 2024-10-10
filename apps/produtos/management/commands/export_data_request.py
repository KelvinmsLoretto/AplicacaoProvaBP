import requests
import csv
import time
import json
import re
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Exporta dados de produtos usando uma request'

    def handle(self, *args, **options):
        self.export_data_request()

    def export_data_request(self):
        login_url = 'https://www.saucedemo.com/'
        inventory_url = 'https://www.saucedemo.com/static/js/main.018d2d1e.chunk.js'
        login_payload = {
            'user-name': 'standard_user',
            'password': 'secret_sauce'
        }

        with requests.Session() as session:
            start_time = time.time()

            session.post(login_url, data=login_payload)

            response = session.get(inventory_url)

            content = response.text
            if content:
                parts = content.split('D=[')
                extracted_data = []
                for part in parts[1:]:
                    parted_json = part.split(']')[0]
                    items = parted_json.split('},')
                    for item in items:
                        item = item.replace("}", "") + '}'
                        item = re.sub(r'(\w+):', r'"\1":', item)
                        try:
                            item_dict = json.loads(item)
                            extracted_data.append({
                                'nome': item_dict.get('name', ''),
                                'descricao': item_dict.get('desc', ''),
                                'preco': item_dict.get('price', '')
                            })
                        except json.JSONDecodeError:
                            continue

                with open('produtos_request.csv', mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=['nome', 'descricao', 'preco'])
                    writer.writeheader()
                    writer.writerows(extracted_data)

                end_time = time.time()
                execution_time = end_time - start_time

                self.stdout.write(self.style.SUCCESS("Dados dos produtos salvos em 'produtos_request.csv'"))
                self.stdout.write(self.style.SUCCESS(f"Tempo de execução: {execution_time:.2f} segundos"))
            else:
                self.stdout.write(self.style.ERROR("Nenhum conteúdo encontrado na resposta."))
