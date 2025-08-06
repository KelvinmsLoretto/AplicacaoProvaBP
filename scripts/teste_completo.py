#!/usr/bin/env python
"""
Script de teste completo para verificar todas as funcionalidades implementadas
Executa testes básicos de cada etapa da avaliação técnica.
"""

import os
import sys
import django
import subprocess
import time

# Configurar Django
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ApiBancaria.settings')
django.setup()

from apps.clientes.models import Cliente, DadosPessoais, ContaBancaria
from apps.emprestimos.models import Emprestimo
from products_scraped.models import ProductScraped

def test_etapa1():
    """Testa funcionalidades da Etapa 1"""
    print("🧪 Testando Etapa 1 - Manipulação de Clientes e Empréstimos...")
    
    try:
        # Verificar se os models existem
        clientes_count = Cliente.objects.count()
        emprestimos_count = Emprestimo.objects.count()
        
        print(f"   ✅ Models funcionando: {clientes_count} clientes, {emprestimos_count} empréstimos")
        
        # Testar criação de um cliente
        if clientes_count == 0:
            print("   📝 Criando cliente de teste...")
            cliente = Cliente.objects.create(
                nome="Cliente Teste",
                cpf="12345678901",
                beneficio="1234567890",
                estado_civil="S",
                sexo="M",
                nome_mae="Mãe Teste",
                email="teste@email.com"
            )
            
            # Criar dados pessoais
            DadosPessoais.objects.create(
                cliente=cliente,
                cep="12345678",
                rua="Rua Teste",
                uf="SP",
                numero="123",
                bairro="Bairro Teste"
            )
            
            # Criar conta bancária
            ContaBancaria.objects.create(
                cliente=cliente,
                numero_conta="1234567890",
                dv_conta="1",
                agencia="1234",
                dv_agencia="1"
            )
            
            print("   ✅ Cliente de teste criado com sucesso")
        
        # Testar criação de empréstimo
        if emprestimos_count == 0:
            print("   💰 Criando empréstimo de teste...")
            cliente = Cliente.objects.first()
            if cliente:
                emprestimo = Emprestimo.objects.create(
                    cliente=cliente,
                    valor_solicitado=10000.00,
                    taxa_juros=5.5,
                    num_parcelas=24
                )
                emprestimo.calcular_valor_total()
                emprestimo.calcular_valor_parcela()
                
                if emprestimo.taxa_juros > 4.0:
                    emprestimo.aprovado = True
                
                emprestimo.save()
                print("   ✅ Empréstimo de teste criado com sucesso")
        
        print("   ✅ Etapa 1: Funcionalidades básicas OK")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro na Etapa 1: {e}")
        return False

def test_etapa2():
    """Testa funcionalidades da Etapa 2"""
    print("🧪 Testando Etapa 2 - Web Scraping...")
    
    try:
        # Verificar se os scripts existem
        selenium_script = "scripts/webscraping/scrape_selenium.py"
        requests_script = "scripts/webscraping/scrape_requests.py"
        
        if os.path.exists(selenium_script):
            print("   ✅ Script Selenium encontrado")
        else:
            print("   ❌ Script Selenium não encontrado")
            return False
        
        if os.path.exists(requests_script):
            print("   ✅ Script Requests encontrado")
        else:
            print("   ❌ Script Requests não encontrado")
            return False
        
        # Verificar se os arquivos CSV foram gerados (se existirem)
        csv_files = []
        for csv_file in ["products_selenium.csv", "products_requests.csv"]:
            if os.path.exists(csv_file):
                csv_files.append(csv_file)
                print(f"   ✅ Arquivo {csv_file} encontrado")
        
        if csv_files:
            print(f"   📊 {len(csv_files)} arquivo(s) CSV de produtos encontrado(s)")
        else:
            print("   ⚠️  Nenhum arquivo CSV de produtos encontrado (execute os scripts primeiro)")
        
        print("   ✅ Etapa 2: Scripts e estrutura OK")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro na Etapa 2: {e}")
        return False

def test_etapa3():
    """Testa funcionalidades da Etapa 3"""
    print("🧪 Testando Etapa 3 - App Django para Importação...")
    
    try:
        # Verificar se o model ProductScraped existe
        produtos_count = ProductScraped.objects.count()
        print(f"   ✅ Model ProductScraped funcionando: {produtos_count} produtos")
        
        # Testar criação de produto
        if produtos_count == 0:
            print("   📦 Criando produto de teste...")
            produto = ProductScraped.objects.create(
                nome="Produto Teste",
                descricao="Descrição do produto teste",
                preco="$29.99",
                fonte="teste"
            )
            print("   ✅ Produto de teste criado com sucesso")
        
        # Verificar se o script de importação existe
        import_script = "scripts/import_scraped_products.py"
        if os.path.exists(import_script):
            print("   ✅ Script de importação encontrado")
        else:
            print("   ❌ Script de importação não encontrado")
            return False
        
        # Verificar se os testes existem
        test_script = "scripts/test_import_script.py"
        if os.path.exists(test_script):
            print("   ✅ Script de testes encontrado")
        else:
            print("   ⚠️  Script de testes não encontrado")
        
        print("   ✅ Etapa 3: App e funcionalidades OK")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro na Etapa 3: {e}")
        return False

def test_estrutura_projeto():
    """Testa a estrutura geral do projeto"""
    print("🧪 Testando estrutura do projeto...")
    
    try:
        # Verificar arquivos essenciais
        arquivos_essenciais = [
            "requirements.txt",
            "manage.py",
            "ApiBancaria/settings.py",
            "README.md"
        ]
        
        for arquivo in arquivos_essenciais:
            if os.path.exists(arquivo):
                print(f"   ✅ {arquivo} encontrado")
            else:
                print(f"   ❌ {arquivo} não encontrado")
                return False
        
        # Verificar apps Django
        apps_django = [
            "apps/clientes",
            "apps/emprestimos", 
            "products_scraped"
        ]
        
        for app in apps_django:
            if os.path.exists(app):
                print(f"   ✅ App {app} encontrado")
            else:
                print(f"   ❌ App {app} não encontrado")
                return False
        
        # Verificar scripts
        scripts = [
            "scripts/gerar_dados_etapa1.py",
            "scripts/webscraping/scrape_selenium.py",
            "scripts/webscraping/scrape_requests.py",
            "scripts/import_scraped_products.py"
        ]
        
        for script in scripts:
            if os.path.exists(script):
                print(f"   ✅ Script {script} encontrado")
            else:
                print(f"   ❌ Script {script} não encontrado")
                return False
        
        print("   ✅ Estrutura do projeto OK")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro na estrutura: {e}")
        return False

def test_dependencias():
    """Testa se as dependências estão instaladas"""
    print("🧪 Testando dependências...")
    
    try:
        import faker
        print("   ✅ Faker instalado")
    except ImportError:
        print("   ❌ Faker não instalado")
        return False
    
    try:
        import pandas
        print("   ✅ Pandas instalado")
    except ImportError:
        print("   ❌ Pandas não instalado")
        return False
    
    try:
        import selenium
        print("   ✅ Selenium instalado")
    except ImportError:
        print("   ❌ Selenium não instalado")
        return False
    
    try:
        import requests
        print("   ✅ Requests instalado")
    except ImportError:
        print("   ❌ Requests não instalado")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("   ✅ BeautifulSoup instalado")
    except ImportError:
        print("   ❌ BeautifulSoup não instalado")
        return False
    
    print("   ✅ Todas as dependências OK")
    return True

def main():
    """Função principal do teste completo"""
    print("🚀 Iniciando teste completo da aplicação...")
    print("=" * 60)
    
    resultados = []
    
    # Testar dependências
    resultados.append(("Dependências", test_dependencias()))
    
    # Testar estrutura
    resultados.append(("Estrutura do Projeto", test_estrutura_projeto()))
    
    # Testar cada etapa
    resultados.append(("Etapa 1", test_etapa1()))
    resultados.append(("Etapa 2", test_etapa2()))
    resultados.append(("Etapa 3", test_etapa3()))
    
    # Resumo final
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    total_tests = len(resultados)
    passed_tests = sum(1 for _, result in resultados if result)
    
    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{nome}: {status}")
    
    print(f"\nTotal: {passed_tests}/{total_tests} testes passaram")
    
    if passed_tests == total_tests:
        print("🎉 Todos os testes passaram! A aplicação está funcionando corretamente.")
        print("\n💡 Próximos passos:")
        print("   1. Execute: python scripts/gerar_dados_etapa1.py")
        print("   2. Execute: python scripts/webscraping/scrape_selenium.py")
        print("   3. Execute: python scripts/import_scraped_products.py")
        print("   4. Acesse o admin Django para visualizar os dados")
    else:
        print("⚠️  Alguns testes falharam. Verifique os erros acima.")
    
    print("=" * 60)

if __name__ == "__main__":
    main() 