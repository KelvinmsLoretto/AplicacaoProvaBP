#!/usr/bin/env python
"""
Teste para o script de importação de produtos
Testa funcionalidades do script import_scraped_products.py
"""

import os
import sys
import django
import pandas as pd
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ApiBancaria.settings')
django.setup()

from products_scraped.models import ProductScraped

class TestImportScript:
    """Testes para o script de importação"""
    
    def setup_method(self):
        """Configuração para cada teste"""
        # Limpar produtos existentes
        ProductScraped.objects.all().delete()
        
        # Criar arquivo CSV temporário para teste
        self.temp_dir = tempfile.mkdtemp()
        self.csv_file = os.path.join(self.temp_dir, "test_products.csv")
        
        # Dados de teste
        test_data = {
            'nome': ['Produto Teste 1', 'Produto Teste 2', 'Produto Teste 3'],
            'descricao': ['Descrição 1', 'Descrição 2', 'Descrição 3'],
            'preco': ['$10.00', '$20.00', '$30.00']
        }
        
        df = pd.DataFrame(test_data)
        df.to_csv(self.csv_file, index=False, encoding='utf-8')
    
    def teardown_method(self):
        """Limpeza após cada teste"""
        # Limpar produtos
        ProductScraped.objects.all().delete()
        
        # Remover arquivo temporário
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_verificar_arquivos_csv(self):
        """Testa a função de verificação de arquivos CSV"""
        from scripts.import_scraped_products import verificar_arquivos_csv
        
        # Teste com arquivo existente
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            arquivos = verificar_arquivos_csv()
            self.assertIn('products_selenium.csv', arquivos)
            self.assertIn('products_requests.csv', arquivos)
        
        # Teste sem arquivos
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = False
            arquivos = verificar_arquivos_csv()
            self.assertEqual(len(arquivos), 0)
    
    def test_importar_csv(self):
        """Testa a importação de CSV"""
        from scripts.import_scraped_products import importar_csv
        
        # Importar CSV de teste
        importados, erros = importar_csv(self.csv_file, "teste")
        
        # Verificar resultados
        self.assertEqual(importados, 3)
        self.assertEqual(erros, 0)
        
        # Verificar se produtos foram criados
        produtos = ProductScraped.objects.all()
        self.assertEqual(produtos.count(), 3)
        
        # Verificar dados dos produtos
        produto1 = produtos.filter(nome="Produto Teste 1").first()
        self.assertIsNotNone(produto1)
        self.assertEqual(produto1.descricao, "Descrição 1")
        self.assertEqual(produto1.preco, "$10.00")
        self.assertEqual(produto1.fonte, "teste")
    
    def test_importar_csv_duplicado(self):
        """Testa importação de produtos duplicados"""
        from scripts.import_scraped_products import importar_csv
        
        # Primeira importação
        importados1, erros1 = importar_csv(self.csv_file, "teste")
        self.assertEqual(importados1, 3)
        
        # Segunda importação (deve evitar duplicatas)
        importados2, erros2 = importar_csv(self.csv_file, "teste")
        self.assertEqual(importados2, 0)  # Nenhum produto novo
        
        # Verificar que ainda há apenas 3 produtos
        self.assertEqual(ProductScraped.objects.count(), 3)
    
    def test_importar_csv_arquivo_inexistente(self):
        """Testa importação de arquivo que não existe"""
        from scripts.import_scraped_products import importar_csv
        
        importados, erros = importar_csv("arquivo_inexistente.csv", "teste")
        self.assertEqual(importados, 0)
        self.assertEqual(erros, 0)
    
    def test_limpar_produtos_antigos(self):
        """Testa limpeza de produtos antigos"""
        from scripts.import_scraped_products import limpar_produtos_antigos
        
        # Criar produtos de teste
        ProductScraped.objects.create(
            nome="Produto 1",
            descricao="Descrição 1",
            preco="$10.00",
            fonte="selenium"
        )
        
        ProductScraped.objects.create(
            nome="Produto 2",
            descricao="Descrição 2",
            preco="$20.00",
            fonte="requests"
        )
        
        # Verificar que produtos foram criados
        self.assertEqual(ProductScraped.objects.count(), 2)
        
        # Limpar todos os produtos
        limpar_produtos_antigos()
        self.assertEqual(ProductScraped.objects.count(), 0)
    
    def test_limpar_produtos_por_fonte(self):
        """Testa limpeza de produtos por fonte específica"""
        from scripts.import_scraped_products import limpar_produtos_antigos
        
        # Criar produtos de fontes diferentes
        ProductScraped.objects.create(
            nome="Produto Selenium",
            descricao="Descrição",
            preco="$10.00",
            fonte="selenium"
        )
        
        ProductScraped.objects.create(
            nome="Produto Requests",
            descricao="Descrição",
            preco="$20.00",
            fonte="requests"
        )
        
        # Verificar produtos criados
        self.assertEqual(ProductScraped.objects.count(), 2)
        
        # Limpar apenas produtos selenium
        limpar_produtos_antigos("selenium")
        self.assertEqual(ProductScraped.objects.count(), 1)
        
        # Verificar que apenas o produto requests permaneceu
        produto_restante = ProductScraped.objects.first()
        self.assertEqual(produto_restante.fonte, "requests")
    
    def test_gerar_relatorio(self):
        """Testa geração de relatório"""
        from scripts.import_scraped_products import gerar_relatorio
        
        # Criar produtos para teste
        ProductScraped.objects.create(
            nome="Produto 1",
            descricao="Descrição 1",
            preco="$10.00",
            fonte="selenium"
        )
        
        ProductScraped.objects.create(
            nome="Produto 2",
            descricao="Descrição 2",
            preco="$20.00",
            fonte="requests"
        )
        
        # Testar geração de relatório (não deve gerar erro)
        try:
            gerar_relatorio()
            relatorio_ok = True
        except Exception as e:
            relatorio_ok = False
            print(f"Erro ao gerar relatório: {e}")
        
        self.assertTrue(relatorio_ok)

def run_tests():
    """Executa todos os testes"""
    print("🧪 Executando testes do script de importação...")
    
    test_instance = TestImportScript()
    
    # Lista de métodos de teste
    test_methods = [
        'test_verificar_arquivos_csv',
        'test_importar_csv',
        'test_importar_csv_duplicado',
        'test_importar_csv_arquivo_inexistente',
        'test_limpar_produtos_antigos',
        'test_limpar_produtos_por_fonte',
        'test_gerar_relatorio'
    ]
    
    passed = 0
    failed = 0
    
    for method_name in test_methods:
        try:
            # Setup
            test_instance.setup_method()
            
            # Executar teste
            method = getattr(test_instance, method_name)
            method()
            
            print(f"✅ {method_name}")
            passed += 1
            
        except Exception as e:
            print(f"❌ {method_name}: {e}")
            failed += 1
        
        finally:
            # Teardown
            test_instance.teardown_method()
    
    print(f"\n📊 Resultados: {passed} passaram, {failed} falharam")
    
    if failed == 0:
        print("🎉 Todos os testes passaram!")
    else:
        print("⚠️  Alguns testes falharam!")

if __name__ == "__main__":
    run_tests() 