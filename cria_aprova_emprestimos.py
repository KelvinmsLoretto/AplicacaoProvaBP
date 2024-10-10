import os
import random
from faker import Faker
import django
import requests

print("Iniciando o script...")

BASE_URL = "http://localhost:8000/api/v1"

def buscaTodosClientes():
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
        "valor_solicitado": random.randint(7, 999),
        "taxa_juros": random.randint(4, 6),
        "num_parcelas": random.randint(1, 7)
    }

    response = requests.post(base_url, json=dados_emprestimo)

    if response.status_code == 201:
        print("Empréstimo criado com sucesso:")
        print(response.json())
    else:
        print(f"Erro ao criar empréstimo: {response.status_code}, {response.text}")


def aprovaEmprestimo(cpf):
    #Consulta ID do Emprestimo 
    base_url_consulta_emprestimos = f"{BASE_URL}/emprestimos/clientes/{cpf}/emprestimos/"
    response_consulta = requests.get(base_url_consulta_emprestimos)
    if response_consulta.status_code == 200:
        for emprestimo in response_consulta.json():
            print('Emprestimo encontrado')
            #Aprova emprestimo para todos Emprestimos do Cliente
            if emprestimo['taxa_juros'] > 4 :
                uuid = emprestimo['id']
                base_url_aprovar_emprestimo = f"{BASE_URL}/emprestimos/{uuid}/aprovar/"
                responseAprova = requests.post(base_url_aprovar_emprestimo)
                if responseAprova.status_code == 200:
                    print(f"Emprestimo {uuid} aprovado com sucesso")
                else:
                    print(f"Erro ao aprovar emprestimo: {responseAprova.status_code}")
            else:
                print('Taxa de Juros menor que 4%, não é possivel aprovar o emprestimo')
    else:
        print(f"Erro ao aprovar emprestimo: {response_consulta.status_code}")

      
def main():
    clients = buscaTodosClientes()
    if not clients:
        print("Nenhum cliente encontrado ou erro ao obter clientes.")
        return
    
    for client in clients:
        print(f"Cliente {client['nome']} com o CPF {client['cpf']} \n")
        escolha = int(input('Você deseja [1] Simular [2]  Criar Emprestimo [3] Aprovar Emprestimo: [4] Criar e Aprovar Emprestimo '))
        if escolha == 1:
            simula(client['cpf'])
        if escolha == 2:
            criar_emprestimo(client['cpf'])
        if escolha == 3:
            aprovaEmprestimo(client['cpf'])
        if escolha == 4:
            criar_emprestimo(client['cpf'])
            aprovaEmprestimo(client['cpf'])

if __name__ == "__main__":
    main()
