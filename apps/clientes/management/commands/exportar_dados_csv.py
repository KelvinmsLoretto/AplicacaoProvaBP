import csv
from django.core.management.base import BaseCommand
from apps.clientes.models import Cliente
from apps.emprestimos.models import Emprestimo

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--arquivo', type=str, default='clientes_emprestimos.csv'
        )

    def handle(self, *args, **kwargs):
        arquivo_csv = kwargs['arquivo']

        with open(arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                'Nome do Cliente', 'CPF', 'Benefício', 'Email', 'Estado Civil', 'Sexo',
                'Valor Solicitado', 'Taxa de Juros', 'Número de Parcelas', 'Valor Total', 
                'Valor da Parcela', 'Aprovado'
            ])

            clientes = Cliente.objects.all()

            for cliente in clientes:
                emprestimos = Emprestimo.objects.filter(cliente=cliente)
                for emprestimo in emprestimos:
                    writer.writerow([
                        cliente.nome, cliente.cpf, cliente.beneficio, cliente.email, 
                        cliente.get_estado_civil_display(), cliente.get_sexo_display(),
                        emprestimo.valor_solicitado, emprestimo.taxa_juros, 
                        emprestimo.num_parcelas, emprestimo.valor_total, 
                        emprestimo.valor_parcela, 'Sim' if emprestimo.aprovado else 'Não'
                    ])

        self.stdout.write(self.style.SUCCESS(f'Dados exportados com sucesso para {arquivo_csv}'))
