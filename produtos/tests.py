# produtos/tests.py

import os
from decimal import Decimal
from django.test import TestCase
from django.core.management import call_command
from django.conf import settings
from django.core.exceptions import ValidationError
from .models import Product
from io import StringIO

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            description='A product for testing.',
            price=Decimal('19.99')
        )

    def test_product_creation(self):
        """Teste a criação de um produto."""
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.description, 'A product for testing.')
        self.assertEqual(self.product.price, Decimal('19.99'))

    def test_str_representation(self):
        """Teste a representação em string do produto."""
        self.assertEqual(str(self.product), 'Test Product')

    def test_price_must_be_positive(self):
        """Teste se o preço do produto deve ser positivo."""
        self.product.price = Decimal('-10.00')
        with self.assertRaises(ValidationError):
            self.product.full_clean()

class ImportProductsCommandTest(TestCase):
    def setUp(self):
        # Conteúdo do CSV de teste
        self.csv_content = """Nome do Produto,Descrição,Preço
Test Product 1,Description 1,10.99
Test Product 2,Description 2,20.99
Invalid Price Product,Description 3,$invalid_price
Incomplete Product,Description 4,
"""
        # Caminho para o arquivo CSV de teste
        self.csv_path = os.path.join(settings.BASE_DIR, 'test_products.csv')
        with open(self.csv_path, 'w', newline='', encoding='utf-8') as file:
            file.write(self.csv_content)

    def tearDown(self):
        # Remove o arquivo CSV de teste após os testes
        if os.path.exists(self.csv_path):
            os.remove(self.csv_path)

    def test_import_products(self):
        """Teste a importação de produtos a partir de um CSV."""
        # Captura a saída do comando
        out = StringIO()
        call_command('import_products', self.csv_path, stdout=out)

        # Verifica se apenas os produtos válidos foram importados
        self.assertEqual(Product.objects.count(), 2)
        product1 = Product.objects.get(name='Test Product 1')
        product2 = Product.objects.get(name='Test Product 2')
        self.assertEqual(product1.description, 'Description 1')
        self.assertEqual(product1.price, Decimal('10.99'))
        self.assertEqual(product2.description, 'Description 2')
        self.assertEqual(product2.price, Decimal('20.99'))

        # Verifica se produtos com preços inválidos não foram importados
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(name='Invalid Price Product')
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(name='Incomplete Product')

        # Verifica as mensagens de saída
        output = out.getvalue()
        self.assertIn('Produto criado: Test Product 1', output)
        self.assertIn('Produto criado: Test Product 2', output)
        self.assertIn("Preço inválido para o produto 'Invalid Price Product': $invalid_price", output)
        self.assertIn("Linha incompleta: {'Nome do Produto': 'Incomplete Product', 'Descrição': 'Description 4', 'Preço': ''}", output)
