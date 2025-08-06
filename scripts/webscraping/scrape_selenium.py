#!/usr/bin/env python
"""
Script de Web Scraping usando Selenium
Coleta produtos da página https://www.saucedemo.com/
Salva dados em CSV com nome, descrição e preço dos produtos.
"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def configurar_driver():
    """Configura o driver do Chrome com opções headless"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executar sem interface gráfica
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"❌ Erro ao configurar driver Chrome: {e}")
        print("💡 Certifique-se de ter o ChromeDriver instalado")
        return None

def coletar_credenciais_disponiveis(driver):
    """Coleta os usuários e senha disponíveis da página de login"""
    try:
        # Navegar para a página
        driver.get("https://www.saucedemo.com/")
        
        # Aguardar carregamento da página
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "login_credentials"))
        )
        
        # Encontrar a seção de credenciais
        credentials_section = driver.find_element(By.CLASS_NAME, "login_credentials")
        
        # Extrair os usuários e senha disponíveis
        usuarios = []
        senha = None
        
        try:
            # Procurar por elementos que contenham os usuários e senha
            credential_items = credentials_section.find_elements(By.TAG_NAME, "h4")
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
                
                # Procurar pela senha
                elif text and "password" in text.lower():
                    # Extrair a senha
                    if ":" in text:
                        senha_part = text.split(":")[-1].strip()
                        if senha_part:
                            senha = senha_part
                            print(f"Senha encontrada na interface: {senha}")
        except:
            pass
        
        # Se não encontrou senha, tentar outros métodos
        if not senha:
            try:
                # Procurar pela div específica da senha
                password_div = credentials_section.find_element(By.CLASS_NAME, "login_password")
                if password_div:
                    # Pegar todo o texto da div
                    full_text = password_div.text.strip()
                    print(f"Texto completo da div password: '{full_text}'")
                    # A senha está como texto direto após o h4
                    if "secret_sauce" in full_text:
                        senha = "secret_sauce"
                        print(f"Senha encontrada na div login_password: {senha}")
            except:
                pass
            
            # Se ainda não encontrou, tentar procurar por "secret_sauce" em qualquer lugar
            if not senha:
                try:
                    all_elements = credentials_section.find_elements(By.XPATH, ".//*")
                    for element in all_elements:
                        text = element.text.strip()
                        if "secret_sauce" in text.lower():
                            senha = "secret_sauce"
                            print(f"Senha encontrada via busca por 'secret_sauce': {senha}")
                            break
                except Exception as e:
                    print(f"Erro ao procurar senha: {e}")
                    pass
            
            # Se ainda não encontrou, usar senha conhecida
            if not senha:
                senha = "secret_sauce"
                print(f"Usando senha padrão: {senha}")
        
        # Se não encontrou usuários, usar lista conhecida
        if not usuarios:
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

def testar_login_com_usuarios(driver, usuarios, senha):
    """Testa login com cada usuário e coleta produtos de cada um"""
    resultados = {}
    
    for usuario in usuarios:
        print(f"\nTentando login com usuário: {usuario}")
        
        try:
            # Navegar para a página de login
            driver.get("https://www.saucedemo.com/")
            
            # Aguardar carregamento da página
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "user-name"))
            )
            
            # Preencher credenciais
            username_field = driver.find_element(By.ID, "user-name")
            password_field = driver.find_element(By.ID, "password")
            
            # Limpar campos
            username_field.clear()
            password_field.clear()
            
            username_field.send_keys(usuario)
            password_field.send_keys(senha)
            
            # Clicar no botão de login
            login_button = driver.find_element(By.ID, "login-button")
            login_button.click()
            
            # Aguardar redirecionamento ou erro
            try:
                # Tentar aguardar pela página de produtos
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
                )
                print(f"Login realizado com sucesso usando usuário: {usuario}")
                
                # Coletar produtos deste usuário
                produtos = coletar_produtos(driver, usuario)
                if produtos:
                    resultados[usuario] = produtos
                    print(f"Coletados {len(produtos)} produtos do usuário {usuario}")
                else:
                    print(f"Nenhum produto coletado do usuário {usuario}")
                    
            except TimeoutException:
                # Verificar se há mensagem de erro
                try:
                    error_element = driver.find_element(By.CLASS_NAME, "error-message-container")
                    error_text = error_element.text
                    print(f"Login falhou para {usuario}: {error_text}")
                except:
                    print(f"Login falhou para {usuario}: Timeout")
                continue
            except Exception as e:
                print(f"Erro inesperado para {usuario}: {e}")
                continue
                
        except Exception as e:
            print(f"Erro ao tentar login com {usuario}: {e}")
            continue
    
    print(f"\nTotal de usuários com produtos coletados: {len(resultados)}")
    return resultados

def fazer_login(driver, username="standard_user", password="secret_sauce"):
    """Faz login na página de demonstração"""
    try:
        # Navegar para a página
        driver.get("https://www.saucedemo.com/")
        
        # Aguardar carregamento da página
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )
        
        # Preencher credenciais
        username_field = driver.find_element(By.ID, "user-name")
        password_field = driver.find_element(By.ID, "password")
        
        username_field.send_keys(username)
        password_field.send_keys(password)
        
        # Clicar no botão de login
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()
        
        # Aguardar redirecionamento
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )
        
        print("✅ Login realizado com sucesso!")
        return True
        
    except TimeoutException:
        print("❌ Timeout ao fazer login")
        return False
    except Exception as e:
        print(f"❌ Erro ao fazer login: {e}")
        return False

def coletar_produtos(driver, username):
    """Coleta dados dos produtos da página"""
    produtos = []
    
    try:
        # Aguardar carregamento da lista de produtos
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
        )
        
        # Encontrar todos os produtos
        items = driver.find_elements(By.CLASS_NAME, "inventory_item")
        
        print(f"Encontrados {len(items)} produtos")
        
        for item in items:
            try:
                # Extrair nome do produto
                nome = item.find_element(By.CLASS_NAME, "inventory_item_name").text
                
                # Extrair descrição do produto
                descricao = item.find_element(By.CLASS_NAME, "inventory_item_desc").text
                
                # Extrair preço do produto
                preco = item.find_element(By.CLASS_NAME, "inventory_item_price").text
                
                produtos.append({
                    'username': username,
                    'nome': nome,
                    'descricao': descricao,
                    'preco': preco
                })
                
                print(f"   Coletado: {nome} - {preco}")
                
            except NoSuchElementException as e:
                print(f"Erro ao coletar produto: {e}")
                continue
        
        return produtos
        
    except Exception as e:
        print(f"Erro ao coletar produtos: {e}")
        return []

def salvar_csv_por_usuario(resultados, filename="products_selenium.csv"):
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
    print("Iniciando Web Scraping com Selenium...")
    
    # Configurar driver
    driver = configurar_driver()
    if not driver:
        return
    
    start_time = time.time()
    
    try:
        # Coletar credenciais disponíveis
        usuarios, senha = coletar_credenciais_disponiveis(driver)
        
        # Verificar se as credenciais foram coletadas
        if not usuarios or not senha:
            print("Não foi possível coletar credenciais da interface")
            return
        
        # Testar login com cada usuário e coletar produtos
        resultados = testar_login_com_usuarios(driver, usuarios, senha)
        
        if not resultados:
            print("Nenhum usuário funcionou para login")
            return
        
        # Salvar produtos em CSV
        if salvar_csv_por_usuario(resultados):
            # Calcular tempo de execução
            end_time = time.time()
            execution_time = end_time - start_time
            
            print(f"\nTempo de execução: {execution_time:.2f} segundos")
            print("Web Scraping com Selenium concluído!")
            
            # Retornar tempo para comparação
            return execution_time
        else:
            print("Nenhum produto foi coletado")
            return None
            
    except Exception as e:
        print(f"Erro durante execução: {e}")
        return None
    finally:
        driver.quit()

if __name__ == "__main__":
    main() 