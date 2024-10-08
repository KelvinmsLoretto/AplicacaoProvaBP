# apps/clientes/management/commands/exportar_dados.py

import csv
from django.core.management.base import BaseCommand
from apps.clientes.models import Cliente, DadosPessoais, ContaBancaria

class Command(BaseCommand):
    help = 'Exporta dados de clientes e empréstimos para um arquivo CSV'

    def handle(self, *args, **kwargs):
        export_file = 'data/exported_clientes.csv'
        
        clientes = Cliente.objects.all()
        with open(export_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['nome', 'email', 'telefone', 'dados_pessoais', 'conta_bancaria']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for cliente in clientes:
                dados_pessoais = DadosPessoais.objects.filter(cliente=cliente).first()
                conta_bancaria = ContaBancaria.objects.filter(cliente=cliente).first()
                writer.writerow({
                    'nome': cliente.nome,
                    'email': cliente.email,
                    'telefone': cliente.telefone,
                    'dados_pessoais': dados_pessoais.to_dict() if dados_pessoais else {},
                    'conta_bancaria': conta_bancaria.to_dict() if conta_bancaria else {}
                })

        self.stdout.write(self.style.SUCCESS(f"Dados exportados com sucesso para '{export_file}'."))

