from django.core.management.base import BaseCommand
from apps.emprestimos.models import Emprestimo
from apps.clientes.models import Cliente
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Gera empréstimos para clientes'

    def handle(self, *args, **kwargs):
        clientes = Cliente.objects.all()
        for cliente in clientes:
            valor_solicitado = Decimal(random.uniform(1000, 5000)).quantize(Decimal('0.01'))
            taxa_juros = Decimal(random.uniform(3.14, 6.5)).quantize(Decimal('0.01'))
            num_parcelas = random.randint(6, 24)

            emprestimo = Emprestimo(
                cliente=cliente,
                valor_solicitado=valor_solicitado,
                taxa_juros=taxa_juros,
                num_parcelas=num_parcelas
            )
            emprestimo.calcular_valor_total()
            emprestimo.calcular_valor_parcela()
            emprestimo.save()

            self.stdout.write(self.style.SUCCESS(f'Empréstimo para {cliente.nome} criado com sucesso.'))
