from django.core.management.base import BaseCommand
from faker import Faker
from apps.clientes.models import Cliente, DadosPessoais, ContaBancaria
import random

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        fake = Faker('pt_BR')
        sexos = ['M', 'F']
        estados_civis = ['S', 'C', 'D', 'V']
        
        for i in range(50):
            nome = fake.name()
            cpf = fake.unique.cpf()
            beneficio = str(fake.unique.random_number(digits=10))
            estado_civil = random.choice(estados_civis)
            sexo = random.choice(sexos)
            nome_mae = fake.name_female() if sexo == 'M' else fake.name_female()
            nome_pai = fake.name_male() if random.choice([True, False]) else "Nada Consta"
            email = fake.unique.email()
            
            cliente = Cliente.objects.create(
                nome=nome,
                cpf=cpf,
                beneficio=beneficio,
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
                numero=str(fake.building_number()),
                bairro=fake.neighborhood()
            )

            ContaBancaria.objects.create(
                cliente=cliente,
                numero_conta=str(fake.unique.random_number(digits=10)),
                dv_conta=str(random.randint(0, 9)),
                agencia=str(random.randint(1000, 9999)),
                dv_agencia=str(random.randint(0, 9))
            )

        self.stdout.write(self.style.SUCCESS('Clientes cadastrados!'))
