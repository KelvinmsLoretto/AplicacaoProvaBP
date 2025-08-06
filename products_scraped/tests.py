from django.test import TestCase
from django.utils import timezone
from .models import ProductScraped

class ProductScrapedModelTest(TestCase):
    """Testes para o model ProductScraped"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.produto = ProductScraped.objects.create(
            nome="Teste Produto",
            descricao="Descrição de teste para o produto",
            preco="$29.99",
            fonte="selenium"
        )
    
    def test_criacao_produto(self):
        """Testa se um produto pode ser criado corretamente"""
        self.assertEqual(self.produto.nome, "Teste Produto")
        self.assertEqual(self.produto.descricao, "Descrição de teste para o produto")
        self.assertEqual(self.produto.preco, "$29.99")
        self.assertEqual(self.produto.fonte, "selenium")
        self.assertIsNotNone(self.produto.data_coleta)
    
    def test_str_representation(self):
        """Testa a representação string do modelo"""
        expected = "Teste Produto - $29.99"
        self.assertEqual(str(self.produto), expected)
    
    def test_get_preco_numerico(self):
        """Testa a extração do valor numérico do preço"""
        # Teste com símbolo de dólar
        self.assertEqual(self.produto.get_preco_numerico(), 29.99)
        
        # Teste com real
        produto_real = ProductScraped.objects.create(
            nome="Produto Real",
            descricao="Produto com preço em real",
            preco="R$ 50,00",
            fonte="requests"
        )
        self.assertEqual(produto_real.get_preco_numerico(), 50.0)
        
        # Teste com preço sem símbolo
        produto_simples = ProductScraped.objects.create(
            nome="Produto Simples",
            descricao="Produto com preço simples",
            preco="15.50",
            fonte="selenium"
        )
        self.assertEqual(produto_simples.get_preco_numerico(), 15.5)
        
        # Teste com preço inválido
        produto_invalido = ProductScraped.objects.create(
            nome="Produto Inválido",
            descricao="Produto com preço inválido",
            preco="preço inválido",
            fonte="requests"
        )
        self.assertEqual(produto_invalido.get_preco_numerico(), 0.0)
    
    def test_ordering(self):
        """Testa se os produtos são ordenados por data de coleta decrescente"""
        # Criar produtos com datas diferentes
        produto_antigo = ProductScraped.objects.create(
            nome="Produto Antigo",
            descricao="Produto criado primeiro",
            preco="$10.00",
            fonte="selenium"
        )
        
        # Aguardar um pouco para garantir diferença de tempo
        import time
        time.sleep(0.1)
        
        produto_novo = ProductScraped.objects.create(
            nome="Produto Novo",
            descricao="Produto criado depois",
            preco="$20.00",
            fonte="requests"
        )
        
        # Verificar ordenação
        produtos_ordenados = ProductScraped.objects.all()
        self.assertEqual(produtos_ordenados[0], produto_novo)
        self.assertEqual(produtos_ordenados[1], produto_antigo)
    
    def test_fonte_default(self):
        """Testa se a fonte padrão é aplicada corretamente"""
        produto_sem_fonte = ProductScraped.objects.create(
            nome="Produto Sem Fonte",
            descricao="Produto sem especificar fonte",
            preco="$30.00"
        )
        self.assertEqual(produto_sem_fonte.fonte, "saucedemo")
    
    def test_campos_obrigatorios(self):
        """Testa se os campos obrigatórios são validados"""
        # Teste com nome vazio
        with self.assertRaises(Exception):
            ProductScraped.objects.create(
                nome="",
                descricao="Descrição",
                preco="$10.00"
            )
        
        # Teste com descrição vazia (deve funcionar pois TextField permite vazio)
        produto_sem_descricao = ProductScraped.objects.create(
            nome="Produto Sem Descrição",
            descricao="",
            preco="$10.00"
        )
        self.assertEqual(produto_sem_descricao.descricao, "")

class ProductScrapedIntegrationTest(TestCase):
    """Testes de integração para ProductScraped"""
    
    def test_multiplos_produtos_mesma_fonte(self):
        """Testa criação de múltiplos produtos da mesma fonte"""
        produtos = []
        for i in range(5):
            produto = ProductScraped.objects.create(
                nome=f"Produto {i+1}",
                descricao=f"Descrição do produto {i+1}",
                preco=f"${(i+1)*10}.99",
                fonte="selenium"
            )
            produtos.append(produto)
        
        # Verificar se todos foram criados
        self.assertEqual(ProductScraped.objects.count(), 5)
        
        # Verificar se todos são da mesma fonte
        produtos_selenium = ProductScraped.objects.filter(fonte="selenium")
        self.assertEqual(produtos_selenium.count(), 5)
    
    def test_produtos_diferentes_fontes(self):
        """Testa criação de produtos de fontes diferentes"""
        # Criar produtos de fontes diferentes
        ProductScraped.objects.create(
            nome="Produto Selenium",
            descricao="Produto coletado via Selenium",
            preco="$25.00",
            fonte="selenium"
        )
        
        ProductScraped.objects.create(
            nome="Produto Requests",
            descricao="Produto coletado via Requests",
            preco="$30.00",
            fonte="requests"
        )
        
        # Verificar contagem por fonte
        self.assertEqual(ProductScraped.objects.filter(fonte="selenium").count(), 1)
        self.assertEqual(ProductScraped.objects.filter(fonte="requests").count(), 1)
        self.assertEqual(ProductScraped.objects.count(), 2)
    
    def test_busca_produtos(self):
        """Testa funcionalidades de busca de produtos"""
        # Criar produtos para teste
        ProductScraped.objects.create(
            nome="Camiseta Azul",
            descricao="Camiseta azul de algodão",
            preco="$29.99",
            fonte="selenium"
        )
        
        ProductScraped.objects.create(
            nome="Calça Jeans",
            descricao="Calça jeans azul",
            preco="$59.99",
            fonte="requests"
        )
        
        ProductScraped.objects.create(
            nome="Tênis Esportivo",
            descricao="Tênis para corrida",
            preco="$89.99",
            fonte="selenium"
        )
        
        # Teste de busca por nome
        produtos_camiseta = ProductScraped.objects.filter(nome__icontains="Camiseta")
        self.assertEqual(produtos_camiseta.count(), 1)
        
        # Teste de busca por descrição
        produtos_azul = ProductScraped.objects.filter(descricao__icontains="azul")
        self.assertEqual(produtos_azul.count(), 2)
        
        # Teste de busca por fonte
        produtos_selenium = ProductScraped.objects.filter(fonte="selenium")
        self.assertEqual(produtos_selenium.count(), 2)
