from django.core.management.base import BaseCommand
from random import randint, uniform
import requests
from typing import Dict, Any

class Command(BaseCommand):
    BASE_URL = 'http://127.0.0.1:8080/api/v1'

    def calcular_valor_total(self, emprestimo_data: Dict[str, Any]) -> float:
        juros_compostos = (1 + (emprestimo_data['taxa_juros'] / 100)) ** emprestimo_data['num_parcelas']
        emprestimo_data['valor_total'] = round(emprestimo_data['valor_solicitado'] * juros_compostos, 2)
        return emprestimo_data['valor_total']

    def handle(self, *args, **kwargs):
        try:
            clientes_response = requests.get(f'{self.BASE_URL}/cliente/clientes/')
            clientes_response.raise_for_status()
            clientes = clientes_response.json()

            for cliente in clientes:
                emprestimos_response = requests.get(f'{self.BASE_URL}/emprestimos/clientes/{cliente["cpf"]}/emprestimos')
                emprestimos_response.raise_for_status()
                emprestimos = emprestimos_response.json()

                if not emprestimos:
                    valor_solicitado = 5000 #mock
                    taxa_juros = 4
                    num_parcelas = 2
                    
                    emprestimo_data = {
                        'valor_solicitado': valor_solicitado,
                        'taxa_juros': taxa_juros,
                        'num_parcelas': num_parcelas,
                    }

                    valor_total_emprestimo = self.calcular_valor_total(emprestimo_data)

                    try:
                        emprestimo_response = requests.post(f'{self.BASE_URL}/emprestimos/clientes/{str(cliente["cpf"])}/emprestimos/criar/', json=emprestimo_data)
                        emprestimo_response.raise_for_status()
                        self.stdout.write(self.style.SUCCESS(f'Empréstimo cadastrado com sucesso para o cliente {cliente["nome"]}!'))
                    except requests.RequestException as e:
                        self.stdout.write(self.style.ERROR(f'Erro ao processar empréstimos: {e}'))

        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Erro ao processar empréstimos: {e}'))

        self.stdout.write(self.style.SUCCESS('Processo de cadastro de empréstimos concluído!'))
