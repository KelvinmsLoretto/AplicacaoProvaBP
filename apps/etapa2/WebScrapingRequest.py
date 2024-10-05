import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Faz o request da página
start_time = time.time()

url = 'https://www.saucedemo.com/inventory.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Coleta os dados dos produtos
produtos = soup.find_all(class_='inventory_item')
dados_produtos = []
for produto in produtos:
    nome = produto.find(class_='inventory_item_name').text
    descricao = produto.find(class_='inventory_item_desc').text
    preco = produto.find(class_='inventory_item_price').text
    dados_produtos.append({'nome': nome, 'descricao': descricao, 'preco': preco})

# Salva os dados em um arquivo CSV
df = pd.DataFrame(dados_produtos)
df.to_csv('produtos_requests.csv', index=False)

# Calculando o tempo de execução
end_time = time.time()
print("Arquivo CSV gerado com sucesso com Requests!")
print(f"Tempo de execução com Requests: {end_time - start_time} segundos")
