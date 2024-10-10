from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from apps.loja.models import Produto

class Command(BaseCommand):
    help = 'Faz o scraping de produtos e salva no banco de dados'

    def handle(self, *args, **kwargs):
        driver = webdriver.Chrome(service=Service('C:/windows/chromedriver.exe'))
        driver.get('https://www.saucedemo.com/')

        username = driver.find_element(By.ID, 'user-name')
        password = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.ID, 'login-button')

        username.send_keys('standard_user')
        password.send_keys('secret_sauce')
        login_button.click()

        time.sleep(3)

        produtos = driver.find_elements(By.CLASS_NAME, 'inventory_item')

        for produto in produtos:
            nome = produto.find_element(By.CLASS_NAME, 'inventory_item_name').text
            preco = produto.find_element(By.CLASS_NAME, 'inventory_item_price').text
            preco_float = float(preco.replace('$', ''))

            produto_obj = Produto(titulo=nome, preco=preco_float)
            produto_obj.save()

        driver.quit()
        self.stdout.write(self.style.SUCCESS('Produtos salvos com sucesso!'))
