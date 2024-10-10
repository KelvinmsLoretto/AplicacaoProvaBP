from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

class Command(BaseCommand):
    help = 'Exporta dados de produtos usando Selenium'

    def handle(self, *args, **options):
        self.export_data_selenium()

    def export_data_selenium(self):
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        try:
            login_url = 'https://www.saucedemo.com/'
            inventory_url = 'https://www.saucedemo.com/inventory.html'

            start_time = time.time()

            driver.get(login_url)
            
            driver.find_element(By.ID, 'user-name').send_keys('standard_user')
            driver.find_element(By.ID, 'password').send_keys('secret_sauce')
            driver.find_element(By.ID, 'login-button').click()
            
            driver.get(inventory_url)
            
            time.sleep(0.5)

            produtos = driver.find_elements(By.CLASS_NAME, 'inventory_item_description')
            dados_produtos = []
            for produto in produtos:
                nome = produto.find_element(By.CLASS_NAME, 'inventory_item_name').text
                descricao = produto.find_element(By.CLASS_NAME, 'inventory_item_desc').text
                preco = produto.find_element(By.CLASS_NAME, 'inventory_item_price').text
                dados_produtos.append({'nome': nome, 'descricao': descricao, 'preco': preco})

            with open('produtos_selenium.csv', mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['nome', 'descricao', 'preco'])
                writer.writeheader()
                writer.writerows(dados_produtos)

            end_time = time.time()
            execution_time = end_time - start_time

            self.stdout.write(self.style.SUCCESS("Dados dos produtos salvos em 'produtos_selenium.csv'"))
            self.stdout.write(self.style.SUCCESS(f"Tempo de execução: {execution_time:.2f} segundos"))
        finally:
            driver.quit()
