import os
import json
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings  # Adicione esta linha
from apps.clientes.models import Cliente, DadosPessoais, ContaBancaria

class Command(BaseCommand):
    help = 'Importa clientes a partir de um arquivo JSON'

    def handle(self, *args, **kwargs):
        # Caminho absoluto para o arquivo JSON na pasta data/
        json_file = os.path.join(settings.BASE_DIR, 'data', 'clientes.json')
        
        if not os.path.exists(json_file):
            self.stdout.write(self.style.ERROR(f'Arquivo "{json_file}" não encontrado.'))
            return
        
        with open(json_file, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                self.stdout.write(self.style.ERROR(f'Erro ao decodificar JSON: {e}'))
                return

            for item in data:
                try:
                    conta_bancaria_data = item.pop('conta_bancaria')
                    dados_pessoais_data = item.pop('dados_pessoais')

                    # Criação do Cliente
                    cliente, created = Cliente.objects.get_or_create(**item)

                    # Criação ou atualização de DadosPessoais
                    DadosPessoais.objects.update_or_create(cliente=cliente, defaults=dados_pessoais_data)

                    # Criação ou atualização de ContaBancaria
                    ContaBancaria.objects.update_or_create(cliente=cliente, defaults=conta_bancaria_data)

                    status = "criado" if created else "atualizado"
                    self.stdout.write(self.style.SUCCESS(f'Cliente {cliente.nome} {status} com sucesso.'))
                
                except KeyError as e:
                    self.stdout.write(self.style.WARNING(f'Dados faltando para o cliente: {e}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Erro ao importar cliente {item.get("nome", "Unknown")}: {e}'))
