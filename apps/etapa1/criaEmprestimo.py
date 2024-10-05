import os
import random
from faker import Faker
import django
import requests

print("Iniciando o script...")

BASE_URL = "http://localhost:8000/api/v1"

def get_all_clients():
    url = f"{BASE_URL}/cliente/clientes/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter clientes: {e}")
        return []

def simula(cpf):
    base_url = f"{BASE_URL}/emprestimos/clientes/{cpf}/emprestimos/simular/"
    
    dados_cliente = {
        "valor_solicitado": 100.0,
        "taxa_juros": 5,
        "num_parcelas": 7
    }

    response = requests.post(base_url, json=dados_cliente)
    
    if response.status_code == 200:
        print("Simulação realizada com sucesso:")
        print(response.json())
    else:
        print(f"Erro ao simular: {response.status_code}, {response.text}")

def criar_emprestimo(cpf):
    base_url = f"{BASE_URL}/emprestimos/clientes/{cpf}/emprestimos/criar/"
    
    dados_emprestimo = {
        "valor_solicitado": random.uniform(7, 999),
        "taxa_juros": random.uniform(4, 6),
        "num_parcelas": random.randint(1, 7)
    }

    response = requests.post(base_url, json=dados_emprestimo)

    if response.status_code == 201:
        print("Empréstimo criado com sucesso:")
        print(response.json())
    else:
        print(f"Erro ao criar empréstimo: {response.status_code}, {response.text}")

def main():
    clients = get_all_clients()
    if not clients:
        print("Nenhum cliente encontrado ou erro ao obter clientes.")
        return
    
    for client in clients:
        print(f"{client['cpf']} \n")
        # simula(client['cpf'])
        criar_emprestimo(client['cpf'])

if __name__ == "__main__":
    main()
