from django.core.management.base import BaseCommand
from apps.emprestimos.models import Emprestimo

class Command(BaseCommand):
    help = 'Deleta todos os empréstimos'

    def handle(self, *args, **kwargs):
        Emprestimo.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Todos os empréstimos foram deletados com sucesso!'))
