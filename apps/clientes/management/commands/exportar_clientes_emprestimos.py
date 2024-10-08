# apps/clientes/management/commands/exportar_clientes_emprestimos.py

import csv
from django.core.management.base import BaseCommand
from apps.clientes.models import Cliente, DadosPessoais, ContaBancaria
from apps.emprestimos.models import Emprestimo

class Command(BaseCommand):
    help = 'Exporta dados de clientes e seus empréstimos para um arquivo CSV'

    def handle(self, *args, **kwargs):
        export_file = 'clientes_emprestimos.csv'

        # Definir os campos para o CSV
        fieldnames = [
            'cliente_id',
            'nome',
            'email',
            'telefone',
            'dados_pessoais',
            'conta_bancaria',
            'emprestimo_id',
            'valor_solicitado',
            'taxa_juros',
            'num_parcelas',
            'valor_total',
            'valor_parcela',
            'aprovado'
        ]

        with open(export_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            clientes = Cliente.objects.all()
            for cliente in clientes:
                dados_pessoais = DadosPessoais.objects.filter(cliente=cliente).first()
                conta_bancaria = ContaBancaria.objects.filter(cliente=cliente).first()
                emprestimos = Emprestimo.objects.filter(cliente=cliente)

                for emprestimo in emprestimos:
                    writer.writerow({
                        'cliente_id': cliente.id,
                        'nome': cliente.nome,
                        'email': cliente.email,
                        'telefone': cliente.telefone,
                        'dados_pessoais': dados_pessoais.to_dict() if dados_pessoais else {},
                        'conta_bancaria': conta_bancaria.to_dict() if conta_bancaria else {},
                        'emprestimo_id': emprestimo.id,
                        'valor_solicitado': emprestimo.valor_solicitado,
                        'taxa_juros': emprestimo.taxa_juros,
                        'num_parcelas': emprestimo.num_parcelas,
                        'valor_total': emprestimo.valor_total,
                        'valor_parcela': emprestimo.valor_parcela,
                        'aprovado': emprestimo.aprovado
                    })

        self.stdout.write(self.style.SUCCESS(f'Dados exportados com sucesso para {export_file}'))
