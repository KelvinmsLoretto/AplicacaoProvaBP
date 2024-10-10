import csv
import requests
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--arquivo', type=str, default='clientes_emprestimos.csv'
        )

    def handle(self, *args, **kwargs):
        arquivo_csv = kwargs['arquivo']

        clientes_url = 'http://127.0.0.1:8080/api/v1/cliente/clientes'
        emprestimos_url_template = 'http://127.0.0.1:8080/api/v1/emprestimos/clientes/{cpf}/emprestimos'

        response = requests.get(clientes_url)
        clientes = response.json()

        with open(arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                'Nome do Cliente', 'CPF', 'Benefício', 'Email', 'Estado Civil', 'Sexo',
                'Valor Solicitado', 'Taxa de Juros', 'Número de Parcelas', 'Valor Total', 
                'Valor da Parcela', 'Aprovado'
            ])

            for cliente in clientes:
                emprestimos_url = emprestimos_url_template.format(cpf=cliente['cpf'])
                response = requests.get(emprestimos_url)
                emprestimos = response.json()

                for emprestimo in emprestimos:
                    writer.writerow([
                        cliente['nome'], cliente['cpf'], cliente['beneficio'], cliente['email'], 
                        cliente['estado_civil'], cliente['sexo'],
                        emprestimo['valor_solicitado'], emprestimo['taxa_juros'], 
                        emprestimo['num_parcelas'], emprestimo['valor_total'], 
                        emprestimo['valor_parcela'], 'Sim' if emprestimo['aprovado'] else 'Não'
                    ])

        self.stdout.write(self.style.SUCCESS(f'Dados exportados com sucesso para {arquivo_csv}'))
