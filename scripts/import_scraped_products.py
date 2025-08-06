#!/usr/bin/env python
"""
Script para importar produtos coletados via web scraping
Lê os CSVs gerados pelos scripts de scraping e salva no banco Django.
"""

import os
import sys
import django
import pandas as pd
from datetime import datetime

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ApiBancaria.settings')
django.setup()

from products_scraped.models import ProductScraped

def verificar_arquivos_csv():
    """Verifica quais arquivos CSV estão disponíveis para importação"""
    arquivos_disponiveis = []
    
    # Verificar arquivos de produtos
    if os.path.exists('products_selenium.csv'):
        arquivos_disponiveis.append('products_selenium.csv')
    
    if os.path.exists('products_requests.csv'):
        arquivos_disponiveis.append('products_requests.csv')
    
    return arquivos_disponiveis

def importar_csv(arquivo_csv, fonte):
    """
    Importa produtos de um arquivo CSV para o banco de dados
    
    Args:
        arquivo_csv (str): Caminho do arquivo CSV
        fonte (str): Fonte dos dados (selenium ou requests)
    
    Returns:
        tuple: (total_importados, total_erros)
    """
    try:
        # Ler CSV
        df = pd.read_csv(arquivo_csv, encoding='utf-8')
        
        print(f"📊 Lendo {len(df)} produtos de '{arquivo_csv}'")
        
        total_importados = 0
        total_erros = 0
        
        for index, row in df.iterrows():
            try:
                # Verificar se o produto já existe (evitar duplicatas)
                produto_existente = ProductScraped.objects.filter(
                    nome=row['nome'],
                    fonte=fonte
                ).first()
                
                if produto_existente:
                    print(f"   ⚠️  Produto já existe: {row['nome']}")
                    continue
                
                # Criar novo produto
                produto = ProductScraped.objects.create(
                    nome=row['nome'],
                    descricao=row['descricao'],
                    preco=row['preco'],
                    fonte=fonte
                )
                
                total_importados += 1
                print(f"   ✅ Importado: {row['nome']} - {row['preco']}")
                
            except Exception as e:
                total_erros += 1
                print(f"   ❌ Erro ao importar produto {index}: {e}")
                continue
        
        return total_importados, total_erros
        
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {arquivo_csv}")
        return 0, 0
    except Exception as e:
        print(f"❌ Erro ao ler arquivo {arquivo_csv}: {e}")
        return 0, 0

def limpar_produtos_antigos(fonte=None):
    """
    Remove produtos antigos do banco de dados
    
    Args:
        fonte (str, optional): Se especificado, remove apenas produtos desta fonte
    """
    try:
        if fonte:
            produtos_removidos = ProductScraped.objects.filter(fonte=fonte).delete()
            print(f"🗑️  Removidos {produtos_removidos[0]} produtos da fonte '{fonte}'")
        else:
            produtos_removidos = ProductScraped.objects.all().delete()
            print(f"🗑️  Removidos {produtos_removidos[0]} produtos de todas as fontes")
            
    except Exception as e:
        print(f"❌ Erro ao limpar produtos: {e}")

def gerar_relatorio():
    """Gera um relatório dos produtos importados"""
    try:
        total_produtos = ProductScraped.objects.count()
        produtos_por_fonte = ProductScraped.objects.values('fonte').annotate(
            count=models.Count('id')
        )
        
        print("\n" + "="*50)
        print("📊 RELATÓRIO DE PRODUTOS IMPORTADOS")
        print("="*50)
        print(f"Total de produtos no banco: {total_produtos}")
        
        for item in produtos_por_fonte:
            print(f"Fonte '{item['fonte']}': {item['count']} produtos")
        
        # Produtos mais recentes
        produtos_recentes = ProductScraped.objects.order_by('-data_coleta')[:5]
        if produtos_recentes:
            print("\n🕒 Produtos mais recentes:")
            for produto in produtos_recentes:
                print(f"   • {produto.nome} ({produto.fonte}) - {produto.data_coleta.strftime('%d/%m/%Y %H:%M')}")
        
        print("="*50)
        
    except Exception as e:
        print(f"❌ Erro ao gerar relatório: {e}")

def main():
    """Função principal do script"""
    print("🚀 Iniciando importação de produtos coletados...")
    
    # Verificar arquivos disponíveis
    arquivos_disponiveis = verificar_arquivos_csv()
    
    if not arquivos_disponiveis:
        print("❌ Nenhum arquivo CSV encontrado!")
        print("💡 Execute primeiro os scripts de web scraping:")
        print("   python scripts/webscraping/scrape_selenium.py")
        print("   python scripts/webscraping/scrape_requests.py")
        return
    
    print(f"📁 Arquivos encontrados: {', '.join(arquivos_disponiveis)}")
    
    # Perguntar se deve limpar dados antigos
    print("\n❓ Deseja limpar produtos antigos antes da importação? (s/n): ", end="")
    resposta = input().lower()
    
    if resposta == 's':
        print("🗑️  Limpando produtos antigos...")
        limpar_produtos_antigos()
    
    # Importar cada arquivo
    total_importados = 0
    total_erros = 0
    
    for arquivo in arquivos_disponiveis:
        print(f"\n📥 Importando {arquivo}...")
        
        # Determinar fonte baseado no nome do arquivo
        if 'selenium' in arquivo:
            fonte = 'selenium'
        elif 'requests' in arquivo:
            fonte = 'requests'
        else:
            fonte = 'desconhecida'
        
        importados, erros = importar_csv(arquivo, fonte)
        total_importados += importados
        total_erros += erros
    
    # Gerar relatório final
    print(f"\n✅ Importação concluída!")
    print(f"📊 Total importado: {total_importados}")
    print(f"❌ Total de erros: {total_erros}")
    
    # Gerar relatório detalhado
    gerar_relatorio()

if __name__ == "__main__":
    main() 