from django.core.management.base import BaseCommand
from apps.clientes.models import Cliente, DadosPessoais, ContaBancaria
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Gera 50 clientes falsos usando Faker'

    def handle(self, *args, **kwargs):
        fake = Faker('pt_BR')
        for _ in range(50):
            nome = fake.name()
            cpf = ''.join([str(random.randint(0, 9)) for _ in range(11)])
            beneficio = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            estado_civil = random.choice(['S', 'C', 'D', 'V'])
            sexo = random.choice(['F', 'M'])
            nome_mae = fake.name_female()
            nome_pai = fake.name_male()
            email = fake.email()

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

            cep = fake.postcode()
            rua = fake.street_name()
            uf = fake.estado_sigla()
            numero = fake.building_number()
            bairro = fake.bairro()

            DadosPessoais.objects.create(
                cliente=cliente,
                cep=cep,
                rua=rua,
                uf=uf,
                numero=numero,
                bairro=bairro
            )

            numero_conta = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            dv_conta = str(random.randint(0, 9))
            agencia = ''.join([str(random.randint(0, 9)) for _ in range(4)])
            dv_agencia = str(random.randint(0, 9))

            ContaBancaria.objects.create(
                cliente=cliente,
                numero_conta=numero_conta,
                dv_conta=dv_conta,
                agencia=agencia,
                dv_agencia=dv_agencia
            )

            self.stdout.write(self.style.SUCCESS(f'Cliente {nome} criado com sucesso.'))
