import os
import json
from django.core.management.base import BaseCommand
from apps.clientes.models import Cliente, DadosPessoais, ContaBancaria

class Command(BaseCommand):
    help = 'Importa clientes a partir de um arquivo JSON'

    def handle(self, *args, **kwargs):
        json_file = os.path.join(os.path.dirname(__file__), 'clientes.json')
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                conta_bancaria_data = item.pop('conta_bancaria')
                dados_pessoais_data = item.pop('dados_pessoais')

                # Criação do Cliente
                cliente = Cliente.objects.create(**item)

                # Criação do DadosPessoais
                DadosPessoais.objects.create(cliente=cliente, **dados_pessoais_data)

                # Criação da ContaBancaria
                ContaBancaria.objects.create(cliente=cliente, **conta_bancaria_data)

                self.stdout.write(self.style.SUCCESS(f'Cliente {cliente.nome} importado com sucesso.'))
