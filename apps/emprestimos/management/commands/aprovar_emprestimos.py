from django.core.management.base import BaseCommand
import requests

class Command(BaseCommand):
    BASE_URL = 'http://127.0.0.1:8080/api/v1'

    def handle(self, *args, **kwargs):
        try:
            emprestimos_response = requests.get(f'{self.BASE_URL}/emprestimos/')
            emprestimos_response.raise_for_status()
            emprestimos = emprestimos_response.json()

            for emprestimo in emprestimos:
                if emprestimo['taxa_juros'] > 4 and not emprestimo['aprovado']:
                    emprestimo_id = emprestimo['id']
                    emprestimo['aprovado'] = True

                    update_response = requests.put(f'{self.BASE_URL}/emprestimos/{emprestimo_id}/', json=emprestimo)
                    update_response.raise_for_status()

                    self.stdout.write(self.style.SUCCESS(f'Empréstimo {emprestimo_id} aprovado.'))

        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Erro ao processar empréstimos: {e}'))

        self.stdout.write(self.style.SUCCESS('Processo de aprovação de empréstimos concluído!'))
