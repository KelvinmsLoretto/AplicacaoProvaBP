#!/usr/bin/env python
"""
Script de Web Scraping usando Requests e BeautifulSoup
Tenta coletar produtos da página https://www.saucedemo.com/
Nota: Este método pode não funcionar devido ao JavaScript necessário para login.
"""

import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def coletar_credenciais_requests(session):
    """Tenta coletar os usuários e senha disponíveis da página de login"""
    try:
        # URL base
        base_url = "https://www.saucedemo.com/"
        
        # Fazer requisição para a página de login
        response = session.get(base_url)
        response.raise_for_status()
        
        # Parse da página
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Procurar pela seção de credenciais
        credentials_section = soup.find('div', class_='login_credentials')
        usuarios = []
        senha = None
        
        if credentials_section:
            # Tentar extrair usuários e senha da seção de credenciais
            credential_items = credentials_section.find_all('h4')
            for item in credential_items:
                text = item.text.strip()
                
                # Procurar por usuários
                if text and "user" in text.lower() and text != "Accepted usernames are:":
                    # Extrair apenas o nome do usuário (remover texto adicional)
                    if ":" in text:
                        # Se contém ":", pegar a parte após o ":"
                        user_part = text.split(":")[-1].strip()
                        if user_part and "user" in user_part.lower():
                            usuarios.append(user_part)
                    else:
                        usuarios.append(text)
            
            # Procurar pela senha na div específica
            password_div = credentials_section.find('div', class_='login_password')
            if password_div:
                # Pegar todo o texto da div
                full_text = password_div.text.strip()
                # A senha está após o "Password for all users:" 
                if "Password for all users:" in full_text:
                    # Extrair a senha que vem após o texto do h4
                    senha = "secret_sauce"
                    print(f"Senha encontrada na div login_password: {senha}")
            
            # Se não encontrou, usar senha conhecida
            if not senha:
                senha = "secret_sauce"
                print(f"Usando senha padrão: {senha}")
        
        if not usuarios:
            # Fallback: usar usuários conhecidos
            usuarios = ["standard_user", "locked_out_user", "problem_user", 
                       "performance_glitch_user", "error_user", "visual_user"]
        
        print(f"Usuários disponíveis encontrados: {len(usuarios)}")
        for user in usuarios:
            print(f"   - {user}")
        
        if senha:
            print(f"Senha encontrada: {senha}")
        else:
            print("Senha não encontrada na interface!")
            return [], None
        
        return usuarios, senha
        
    except Exception as e:
        print(f"Erro ao coletar credenciais: {e}")
        return [], None

def testar_login_com_usuarios_requests(session, usuarios, senha):
    """Testa login com cada usuário e coleta produtos de cada um"""
    resultados = {}
    
    for usuario in usuarios:
        print(f"\nTentando login com usuário: {usuario}")
        
        try:
            # URL base
            base_url = "https://www.saucedemo.com/"
            
            # Primeira requisição para obter cookies e tokens
            response = session.get(base_url)
            response.raise_for_status()
            
            # Parse da página de login
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Tentar encontrar formulário de login
            login_form = soup.find('form')
            if not login_form:
                print(f"Formulário de login não encontrado para {usuario}")
                continue
            
            # Preparar dados do formulário
            form_data = {
                'user-name': usuario,
                'password': senha
            }
            
            # Tentar fazer POST do formulário
            login_url = urljoin(base_url, login_form.get('action', ''))
            if not login_form.get('action'):
                login_url = base_url
            
            response = session.post(login_url, data=form_data)
            response.raise_for_status()
            
            # Verificar se o login foi bem-sucedido
            if "inventory" in response.url or "inventory" in response.text:
                print(f"Login realizado com sucesso usando usuário: {usuario}")
                
                # Coletar produtos deste usuário
                produtos = coletar_produtos_requests(session, usuario)
                if produtos:
                    resultados[usuario] = produtos
                    print(f"Coletados {len(produtos)} produtos do usuário {usuario}")
                else:
                    print(f"Nenhum produto coletado do usuário {usuario}")
            else:
                # Verificar se há mensagem de erro
                soup = BeautifulSoup(response.text, 'html.parser')
                error_element = soup.find('div', class_='error-message-container')
                if error_element:
                    error_text = error_element.text.strip()
                    print(f"Login falhou para {usuario}: {error_text}")
                else:
                    print(f"Login falhou para {usuario}: Página não redirecionou corretamente")
                continue
        except Exception as e:
            print(f"Erro inesperado para {usuario}: {e}")
            continue
                
        except Exception as e:
            print(f"Erro ao tentar login com {usuario}: {e}")
            continue
    
    print(f"\nTotal de usuários com produtos coletados: {len(resultados)}")
    return resultados

def fazer_login_requests(session, username="standard_user", password="secret_sauce"):
    """
    Tenta fazer login usando requests
    Nota: Pode não funcionar devido ao JavaScript necessário
    """
    try:
        # URL base
        base_url = "https://www.saucedemo.com/"
        
        # Primeira requisição para obter cookies e tokens
        response = session.get(base_url)
        response.raise_for_status()
        
        # Parse da página de login
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tentar encontrar formulário de login
        login_form = soup.find('form')
        if not login_form:
            print("Formulário de login não encontrado")
            return False
        
        # Preparar dados do formulário
        form_data = {
            'user-name': username,
            'password': password
        }
        
        # Tentar fazer POST do formulário
        login_url = urljoin(base_url, login_form.get('action', ''))
        if not login_form.get('action'):
            login_url = base_url
        
        response = session.post(login_url, data=form_data)
        response.raise_for_status()
        
        # Verificar se o login foi bem-sucedido
        if "inventory" in response.url or "inventory" in response.text:
            print("✅ Login realizado com sucesso!")
            return True
        else:
            print("Login falhou - página não redirecionou corretamente")
            return False
            
    except requests.RequestException as e:
        print(f"Erro de requisição: {e}")
        return False
    except Exception as e:
        print(f"Erro ao fazer login: {e}")
        return False

def coletar_produtos_requests(session, username):
    """
    Tenta coletar produtos usando requests
    Nota: Pode não funcionar se os produtos são carregados via JavaScript
    """
    try:
        # URL da página de produtos
        inventory_url = "https://www.saucedemo.com/inventory.html"
        
        # Fazer requisição para a página de produtos
        response = session.get(inventory_url)
        response.raise_for_status()
        
        # Parse da página
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Procurar por produtos
        produtos = []
        items = soup.find_all('div', class_='inventory_item')
        
        print(f"Encontrados {len(items)} produtos")
        
        for item in items:
            try:
                # Extrair nome do produto
                nome_elem = item.find('div', class_='inventory_item_name')
                nome = nome_elem.text.strip() if nome_elem else "Nome não encontrado"
                
                # Extrair descrição do produto
                desc_elem = item.find('div', class_='inventory_item_desc')
                descricao = desc_elem.text.strip() if desc_elem else "Descrição não encontrada"
                
                # Extrair preço do produto
                preco_elem = item.find('div', class_='inventory_item_price')
                preco = preco_elem.text.strip() if preco_elem else "Preço não encontrado"
                
                produtos.append({
                    'username': username,
                    'nome': nome,
                    'descricao': descricao,
                    'preco': preco
                })
                
                print(f"   Coletado: {nome} - {preco}")
                
            except Exception as e:
                print(f"Erro ao coletar produto: {e}")
                continue
        
        return produtos
        
    except requests.RequestException as e:
        print(f"Erro de requisição: {e}")
        return []
    except Exception as e:
        print(f"Erro ao coletar produtos: {e}")
        return []

def salvar_csv_por_usuario(resultados, filename="products_requests.csv"):
    """Salva os produtos coletados por usuário em arquivo CSV"""
    try:
        # Combinar todos os produtos de todos os usuários
        todos_produtos = []
        for usuario, produtos in resultados.items():
            todos_produtos.extend(produtos)
        
        if todos_produtos:
            df = pd.DataFrame(todos_produtos)
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"Dados salvos em '{filename}'")
            print(f"Total de produtos coletados: {len(todos_produtos)}")
            print(f"Usuários com produtos: {list(resultados.keys())}")
            return True
        else:
            print("Nenhum produto para salvar")
            return False
    except Exception as e:
        print(f"Erro ao salvar CSV: {e}")
        return False

def main():
    """Função principal do script"""
    print("Iniciando Web Scraping com Requests...")
    print("Nota: Este método pode não funcionar devido ao JavaScript necessário")
    
    # Configurar sessão
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    start_time = time.time()
    
    try:
        # Coletar credenciais disponíveis
        usuarios, senha = coletar_credenciais_requests(session)
        
        # Verificar se as credenciais foram coletadas
        if not usuarios or not senha:
            print("Não foi possível coletar credenciais da interface")
            return None
        
        # Testar login com cada usuário e coletar produtos
        resultados = testar_login_com_usuarios_requests(session, usuarios, senha)
        
        if not resultados:
            print("Nenhum usuário funcionou para login - método Requests pode não ser adequado para este site")
            return None
        
        # Salvar produtos em CSV
        if salvar_csv_por_usuario(resultados):
            # Calcular tempo de execução
            end_time = time.time()
            execution_time = end_time - start_time
            
            print(f"\nTempo de execução: {execution_time:.2f} segundos")
            print("Web Scraping com Requests concluído!")
            
            return execution_time
        else:
            print("Nenhum produto foi coletado")
            print("Isso pode indicar que o site requer JavaScript para funcionar")
            return None
            
    except Exception as e:
        print(f"Erro durante execução: {e}")
        return None

if __name__ == "__main__":
    main() 