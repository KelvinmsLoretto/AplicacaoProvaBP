# apps/emprestimos/management/commands/aprovar_emprestimos.py

from django.core.management.base import BaseCommand
from apps.emprestimos.models import Emprestimo

class Command(BaseCommand):
    help = 'Aprova empréstimos com taxa de juros acima de 4%'

    def handle(self, *args, **kwargs):
        # Filtra empréstimos com taxa de juros > 4% e ainda não aprovados
        emprestimos = Emprestimo.objects.filter(taxa_juros__gt=4, aprovado=False)
        total = emprestimos.count()

        if total == 0:
            self.stdout.write(self.style.WARNING("Nenhum empréstimo para aprovar."))
            return

        for emprestimo in emprestimos:
            emprestimo.aprovado = True
            emprestimo.save()
            self.stdout.write(self.style.SUCCESS(f'Empréstimo {emprestimo.id} aprovado.'))

        self.stdout.write(self.style.SUCCESS(f'Total de {total} empréstimos aprovados.'))
