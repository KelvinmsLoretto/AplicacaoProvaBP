from django.core.management.base import BaseCommand
from random import randint, uniform
import requests

class Command(BaseCommand):
    BASE_URL = 'http://127.0.0.1:8080/api/v1'

    def handle(self, *args, **kwargs):
        try:
            clientes_response = requests.get(f'{self.BASE_URL}/cliente/clientes/')
            clientes_response.raise_for_status()
            clientes = clientes_response.json()

            for cliente in clientes:
                valor_solicitado = round(uniform(1000, 50000), 2)
                taxa_juros = round(uniform(1, 10), 2)
                num_parcelas = randint(6, 36)

                emprestimo_data = {
                    'valor_solicitado': valor_solicitado,
                    'taxa_juros': taxa_juros,
                    'num_parcelas': num_parcelas,
                }

                emprestimo_response = requests.post(f'{self.BASE_URL}/emprestimos/clientes/{cliente['id']}/emprestimos/criar', data=emprestimo_data)
                emprestimo_response.raise_for_status()

                self.stdout.write(self.style.SUCCESS(f'Empréstimo cadastrado com sucesso para o cliente {cliente["nome"]}!'))

        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Erro ao processar empréstimos: {e}'))

        self.stdout.write(self.style.SUCCESS('Processo de cadastro de empréstimos concluído!'))
