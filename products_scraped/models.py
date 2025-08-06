from django.db import models

# Create your models here.

class ProductScraped(models.Model):
    """
    Model para armazenar produtos coletados via web scraping
    """
    nome = models.CharField(max_length=255, verbose_name="Nome do Produto")
    descricao = models.TextField(verbose_name="Descrição do Produto")
    preco = models.CharField(max_length=50, verbose_name="Preço do Produto")
    data_coleta = models.DateTimeField(auto_now_add=True, verbose_name="Data de Coleta")
    fonte = models.CharField(max_length=50, default="saucedemo", verbose_name="Fonte dos Dados")
    
    class Meta:
        verbose_name = "Produto Coletado"
        verbose_name_plural = "Produtos Coletados"
        ordering = ['-data_coleta']
    
    def __str__(self):
        return f"{self.nome} - {self.preco}"
    
    def get_preco_numerico(self):
        """
        Tenta extrair o valor numérico do preço
        Remove símbolos de moeda e converte para float
        """
        try:
            # Remove símbolos comuns de moeda e espaços
            preco_limpo = self.preco.replace('$', '').replace('R$', '').replace(' ', '').strip()
            return float(preco_limpo)
        except (ValueError, AttributeError):
            return 0.0
