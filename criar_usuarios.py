import os
import random
from faker import Faker
import django
import sys

print("Iniciando o script...")

# Configura o ambiente Django dinamicamente
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ApiBancaria.settings")

# Adiciona o diretório raiz do projeto ao sys.path
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

django.setup()

# Importar os modelos após configurar o Django
from apps.clientes.models import Cliente, DadosPessoais, ContaBancaria

# Inicializa o Faker
fake = Faker('pt_BR')

def gerar_usuarios(numeroCadastros):
    for _ in range(numeroCadastros):
        nome = fake.name()
        cpf = fake.cpf().replace('.', '').replace('-', '')
        beneficio = fake.random_number(digits=10, fix_len=True)
        estado_civil = random.choice(['S', 'C', 'D', 'V'])
        sexo = random.choice(['F', 'M'])
        nome_mae = fake.name_female() if sexo == 'M' else fake.name_male()
        nome_pai = fake.name_male() if sexo == 'M' else fake.name_female()
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
        uf = fake.state_abbr()
        numero = str(fake.random_number(digits=4, fix_len=False))
        bairro = fake.bairro()

        dadosPessoais = DadosPessoais.objects.create(
            cliente=cliente,
            cep=cep,
            rua=rua,
            uf=uf,
            numero=numero,
            bairro=bairro
        )

        numero_conta = str(fake.random_number(digits=10, fix_len=True))
        dv_conta = str(fake.random_digit())
        agencia = str(fake.random_number(digits=4, fix_len=True))
        dv_agencia = str(fake.random_digit())

        contaBancaria = ContaBancaria.objects.create(
            cliente=cliente,
            numero_conta=numero_conta,
            dv_conta=dv_conta,
            agencia=agencia,
            dv_agencia=dv_agencia
        )

    print("Usuários criados com sucesso!")

if __name__ == "__main__":
    numeroCadastros = int(input('Quantos cadastros você deseja criar? '))
    gerar_usuarios(numeroCadastros)
