from django.core.management.base import BaseCommand
from faker import Faker
from apps.clientes.models import Cliente, DadosPessoais, ContaBancaria
import csv

class Command(BaseCommand):
    help = 'Gera 50 clientes aleatórios usando a biblioteca Faker'

    def handle(self, *args, **kwargs):
        fake = Faker('pt_BR')
        Faker.seed(10)
        
        clientes_data = []

        for _ in range(50):
            nome = fake.name()
            cpf = fake.unique.random_number(digits=11)
            beneficio = fake.random_number(digits=10)
            estado_civil = fake.random_element(elements=("S", "C", "D", "V"))
            sexo = fake.random_element(elements=("F", "M"))
            nome_mae = fake.name_female()
            nome_pai = fake.name_male()
            email = fake.email()

            cliente = Cliente.objects.create(
                nome=nome,
                cpf=str(cpf),
                beneficio=str(beneficio),
                estado_civil=estado_civil,
                sexo=sexo,
                nome_mae=nome_mae,
                nome_pai=nome_pai,
                email=email
            )

            DadosPessoais.objects.create(
                cliente=cliente,
                cep=fake.postcode(),
                rua=fake.street_name(),
                uf=fake.state_abbr(),
                numero=fake.building_number(),
                bairro=fake.bairro()
            )

            ContaBancaria.objects.create(
                cliente=cliente,
                numero_conta=fake.random_number(digits=10),
                dv_conta=fake.random_digit(),
                agencia=fake.random_number(digits=4),
                dv_agencia=fake.random_digit(),
            )

            clientes_data.append({
                'nome': nome,
                'cpf': str(cpf),
                'beneficio': str(beneficio),
                'estado_civil': estado_civil,
                'sexo': sexo,
                'nome_mae': nome_mae,
                'nome_pai': nome_pai,
                'email': email,
                'cep': fake.postcode(),
                'rua': fake.street_name(),
                'uf': fake.state_abbr(),
                'numero': fake.building_number(),
                'bairro': fake.bairro(),
                'numero_conta': fake.random_number(digits=10),
                'dv_conta': fake.random_digit(),
                'agencia': fake.random_number(digits=4),
                'dv_agencia': fake.random_digit(),
            })

        self._save_to_csv(clientes_data)
        self.stdout.write(self.style.SUCCESS('50 clientes gerados com sucesso!'))

    def _save_to_csv(self, clientes_data):
        with open('clientes.csv', mode='w', newline='', encoding='utf-8') as file:
            fieldnames = [
                'nome', 'cpf', 'beneficio', 'estado_civil', 'sexo',
                'nome_mae', 'nome_pai', 'email', 'cep', 'rua',
                'uf', 'numero', 'bairro', 'numero_conta',
                'dv_conta', 'agencia', 'dv_agencia'
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(clientes_data)
