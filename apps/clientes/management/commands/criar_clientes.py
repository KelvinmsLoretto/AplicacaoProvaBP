from django.core.management.base import BaseCommand
from faker import Faker
import random
import requests

class Command(BaseCommand):
    REQUEST_URL = 'http://127.0.0.1:8080/api/v1/cliente/clientes'

    def handle(self, *args, **kwargs):
        fake = Faker('pt_BR')
        sexos = ['M', 'F']
        estados_civis = ['S', 'C', 'D', 'V']
        
        for i in range(50):
            try:
                nome = fake.name()
                cpf = fake.unique.cpf()
                beneficio = str(fake.unique.random_number(digits=10))
                estado_civil = random.choice(estados_civis)
                sexo = random.choice(sexos)
                nome_mae = fake.name_female() if sexo == 'M' else fake.name_female()
                nome_pai = fake.name_male() if random.choice([True, False]) else "Nada Consta"
                email = fake.unique.email()
                


                dados_pessoais = {
                    'cep': fake.postcode(),
                    'rua': fake.street_name(),
                    'uf': fake.state_abbr(),
                    'numero': str(fake.building_number()),
                    'bairro': fake.neighborhood()
                }

                conta_bancaria = {
                    'numero_conta': str(fake.unique.random_number(digits=10)),
                    'dv_conta': str(random.randint(0, 9)),
                    'agencia': str(random.randint(1000, 9999)),
                    'dv_agencia': str(random.randint(0, 9))
                }

                cliente_data = {
                    'nome': nome,
                    'cpf': cpf,
                    'beneficio': beneficio,
                    'estado_civil': estado_civil,
                    'sexo': sexo,
                    'nome_mae': nome_mae,
                    'nome_pai': nome_pai,
                    'email': email,
                    'dados_pessoais': dados_pessoais,
                    'conta_bancaria':conta_bancaria
                }

                cliente_response = requests.post(f'{self.REQUEST_URL}', data=cliente_data)
                
                cliente_response.raise_for_status()

                self.stdout.write(self.style.SUCCESS(f'Cliente {nome} cadastrado com sucesso!'))

            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f'Erro ao cadastrar cliente {nome}: {e}'))

        self.stdout.write(self.style.SUCCESS('Processo de cadastro concluído!'))
