# apps/clientes/models.py

from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True)
    beneficio = models.CharField(max_length=10)
    estado_civil = models.CharField(max_length=20)
    sexo = models.CharField(max_length=10)
    nome_mae = models.CharField(max_length=255)
    nome_pai = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)  # Campo telefone

    def __str__(self):
        return self.nome

class ContaBancaria(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    numero_conta = models.CharField(max_length=20)
    dv_conta = models.CharField(max_length=2)
    agencia = models.CharField(max_length=10)
    dv_agencia = models.CharField(max_length=2)

    def to_dict(self):
        return {
            'numero_conta': self.numero_conta,
            'dv_conta': self.dv_conta,
            'agencia': self.agencia,
            'dv_agencia': self.dv_agencia
        }

class DadosPessoais(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cep = models.CharField(max_length=8)
    rua = models.CharField(max_length=255)
    uf = models.CharField(max_length=2)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)

    def to_dict(self):
        return {
            'cep': self.cep,
            'rua': self.rua,
            'uf': self.uf,
            'numero': self.numero,
            'bairro': self.bairro
        }
