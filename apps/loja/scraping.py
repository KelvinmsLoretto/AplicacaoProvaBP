import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ApiBancaria.settings')
django.setup()

from loja.models import Produto

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
print("Dados dos produtos salvos no banco de dados.")

