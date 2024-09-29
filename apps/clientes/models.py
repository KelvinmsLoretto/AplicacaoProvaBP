from django.db import models

class Cliente(models.Model):
    ESTADO_CIVIL = (
        ("S", "solteiro"),
        ("C", "casado"),
        ("D", "divorciado"),
        ("V", "viuvo")
    )

    SEXO = (
        ("F", "Feminino"),
        ("M", "Masculino"),
    )

    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True, primary_key=True)
    beneficio = models.CharField(max_length=10, unique=True)
    estado_civil = models.CharField(choices=ESTADO_CIVIL, max_length=1)
    sexo = models.CharField(choices=(SEXO), max_length=1)
    nome_mae = models.CharField(max_length=255, blank=False, null=False)
    nome_pai = models.CharField(max_length=255, blank=True, null=True, default="Nada Consta")
    email = models.EmailField()

    def __str__(self):
        return self.nome


class DadosPessoais(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='dados_pessoais') 
    cep = models.CharField(max_length=8)
    rua = models.CharField(max_length=255)
    uf = models.CharField(max_length=2)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=255)

    def __str__(self):
        return f"Endereco {self.rua}"

class ContaBancaria(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='conta_bancaria')
    numero_conta = models.CharField(max_length=10, unique=True)
    dv_conta = models.CharField(max_length=1)
    agencia = models.CharField(max_length=4)
    dv_agencia = models.CharField(max_length=1)
    
    def __str__(self):
        return f"Conta {self.numero_conta} - {self.cliente.nome}"
