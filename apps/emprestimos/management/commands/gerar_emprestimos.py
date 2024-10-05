from django.core.management.base import BaseCommand
from random import randint, uniform
from apps.clientes.models import Cliente
from apps.emprestimos.models import Emprestimo

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        clientes = Cliente.objects.all()

        for cliente in clientes:
            valor_solicitado = round(uniform(1000, 50000), 2) 
            taxa_juros = round(uniform(1, 10), 2)  
            num_parcelas = randint(6, 36)

            emprestimo = Emprestimo.objects.create(
                cliente=cliente,
                valor_solicitado=valor_solicitado,
                taxa_juros=taxa_juros,
                num_parcelas=num_parcelas,
            )

            emprestimo.calcular_valor_total()
            emprestimo.calcular_valor_parcela()

            emprestimo.save()

        self.stdout.write(self.style.SUCCESS('Empréstimos cadastrados com sucesso para todos os clientes.'))
