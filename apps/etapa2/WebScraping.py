import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

# Configuração do Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://www.saucedemo.com/')

# Aguarda a página carregar e faz o login
time.sleep(2)
username = driver.find_element(By.XPATH, '//*[@id="user-name"]')
password = driver.find_element(By.XPATH, '//*[@id="password"]')
login_button = driver.find_element(By.XPATH, '//*[@id="login-button"]')

username.send_keys('standard_user')
password.send_keys('secret_sauce')
login_button.click()

# Aguarda o carregamento da página de produtos
time.sleep(2)

# Medindo o tempo de execução
start_time = time.time()

page_source = driver.page_source

# Usa BeautifulSoup para fazer o parsing do conteúdo da página
soup = BeautifulSoup(page_source, 'html.parser')
produtos = soup.find_all(class_='inventory_item')

# Coleta os dados dos produtos
dados_produtos = []
for produto in produtos:
    nome = produto.find(class_='inventory_item_name').text
    descricao = produto.find(class_='inventory_item_desc').text
    preco = produto.find(class_='inventory_item_price').text
    dados_produtos.append({'nome': nome, 'descricao': descricao, 'preco': preco})

# Fecha o driver
driver.quit()

# Salva os dados em um arquivo CSV
df = pd.DataFrame(dados_produtos)
df.to_csv('produtos_selenium.csv', index=False)

# Calculando o tempo de execução
end_time = time.time()
print("Arquivo CSV gerado com sucesso!")
print(f"Tempo de execução com Selenium: {end_time - start_time} segundos")
