from django.db import models
from apps.clientes.models import Cliente
import uuid

class Emprestimo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='emprestimos')
    valor_solicitado = models.DecimalField(max_digits=10, decimal_places=2)
    taxa_juros = models.DecimalField(max_digits=5, decimal_places=2)
    num_parcelas = models.IntegerField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor_parcela = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    aprovado = models.BooleanField(default=False)
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Empréstimo de {self.valor_solicitado} para {self.cliente.nome}"

    def calcular_valor_total(self):
        juros_compostos = (1 + (self.taxa_juros / 100)) ** self.num_parcelas
        self.valor_total = round(self.valor_solicitado * juros_compostos, ndigits=2)
        return self.valor_total

    def calcular_valor_parcela(self):
        if self.num_parcelas > 0:
            self.valor_parcela = round(self.valor_total / self.num_parcelas, ndigits=2)
        return self.valor_parcela
 