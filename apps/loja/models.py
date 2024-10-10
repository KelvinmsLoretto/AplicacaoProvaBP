from django.db import models

class Produto(models.Model):
   
    titulo = models.CharField(max_length=255, default='Produto Padrão') 
    
    preco = models.DecimalField(max_digits=10, decimal_places=2)
   
    def __str__(self):
        return self.titulo
