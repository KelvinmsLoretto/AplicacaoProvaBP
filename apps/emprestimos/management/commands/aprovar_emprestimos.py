from django.core.management.base import BaseCommand
import requests

class Command(BaseCommand):
    BASE_URL = 'http://127.0.0.1:8080/api/v1'

    def handle(self, *args, **kwargs):
        try:
            clientes_response = requests.get(f'{self.BASE_URL}/cliente/clientes/')
            clientes_response.raise_for_status()
            clientes = clientes_response.json()

            for cliente in clientes:
                emprestimos_response = requests.get(f'{self.BASE_URL}/emprestimos/clientes/{cliente['cpf']}/emprestimos')
                emprestimos_response.raise_for_status()
                emprestimos = emprestimos_response.json()

                for emprestimo in emprestimos:
                    if float(emprestimo['taxa_juros']) >= 4.00 and not emprestimo['aprovado']:
                        update_response = requests.get(f'{self.BASE_URL}/emprestimos/{emprestimo['id']}/aprovar', json=emprestimo)
                        update_response.raise_for_status()
                        self.stdout.write(self.style.SUCCESS(f'Empréstimo {emprestimo['id']} aprovado.'))

        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Erro ao processar empréstimos: {e}'))

        self.stdout.write(self.style.SUCCESS('Processo de aprovação de empréstimos concluído!'))
