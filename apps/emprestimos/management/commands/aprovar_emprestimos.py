from django.core.management.base import BaseCommand
from apps.emprestimos.models import Emprestimo

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        emprestimos = Emprestimo.objects.filter(taxa_juros__gt=4, aprovado=False) # para aprovação

        for emprestimo in emprestimos:
            emprestimo.aprovado = True
            emprestimo.save()

        self.stdout.write(self.style.SUCCESS(f'{emprestimos.count()} empréstimos aprovados.'))
