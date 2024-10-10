import csv
import random
from django.core.management.base import BaseCommand
from apps.emprestimos.models import Emprestimo
from apps.clientes.models import Cliente

class Command(BaseCommand):
    help = 'Gera empréstimos para clientes existentes e salva em CSV'

    def handle(self, *args, **kwargs):
        clientes = Cliente.objects.all()
        emprestimos_data = []

        for cliente in clientes:
            valor = round(random.uniform(1000, 10000), 2)
            taxa_juros = round(random.uniform(1, 10), 2)
            aprovado = taxa_juros > 4

            emprestimo = Emprestimo.objects.create(
                cliente=cliente,
                valor_solicitado=valor,
                taxa_juros=taxa_juros,
                num_parcelas=random.randint(1, 12)
            )

            if aprovado:
                emprestimo.calcular_valor_total()
                emprestimo.calcular_valor_parcela()
                emprestimo.aprovado = True
                emprestimo.save()

            emprestimos_data.append({
                'cliente_cpf': cliente.cpf,
                'valor_solicitado': emprestimo.valor_solicitado,
                'taxa_juros': emprestimo.taxa_juros,
                'aprovado': emprestimo.aprovado
            })

        with open('emprestimos.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['cliente_cpf', 'valor_solicitado', 'taxa_juros', 'aprovado'])
            writer.writeheader()
            writer.writerows(emprestimos_data)

        self.stdout.write(self.style.SUCCESS('Empréstimos gerados e salvos em "emprestimos.csv" com sucesso!'))
