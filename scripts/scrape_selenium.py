# scrape_selenium.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import csv
import time

# Configurações do Selenium
options = Options()
options.headless = True  # Executa o navegador em modo headless (sem interface gráfica)

# Inicializar o driver do Firefox
service = Service()  # O Selenium automaticamente encontrará o geckodriver no PATH

driver = webdriver.Firefox(service=service, options=options)

try:
    # Abrir a página de login
    driver.get('https://www.saucedemo.com/')

    # Preencher os campos de login
    driver.find_element(By.ID, 'user-name').send_keys('standard_user')
    driver.find_element(By.ID, 'password').send_keys('secret_sauce')

    # Clicar no botão de login
    driver.find_element(By.ID, 'login-button').click()

    # Aguardar o carregamento da página de inventário
    time.sleep(2)  # Ajuste o tempo conforme necessário

    # Coletar todos os itens de inventário
    items = driver.find_elements(By.CLASS_NAME, 'inventory_item')

    # Criar e escrever no CSV
    with open('produtos_selenium.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome do Produto', 'Descrição', 'Preço'])

        for item in items:
            nome = item.find_element(By.CLASS_NAME, 'inventory_item_name').text.strip()
            descricao = item.find_element(By.CLASS_NAME, 'inventory_item_desc').text.strip()
            preco = item.find_element(By.CLASS_NAME, 'inventory_item_price').text.strip()
            writer.writerow([nome, descricao, preco])

    print("Dados exportados com sucesso para 'produtos_selenium.csv'.")

finally:
    # Fechar o navegador
    driver.quit()
