import requests
import csv

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

def salvar_clientes_csv(clientes, nome_arquivo):
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['cpf', 'nome', 'email', 'beneficio', 'estado_civil', 'sexo', 'nome_mae', 'nome_pai']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for client in clientes:
            writer.writerow({
                'cpf': client['cpf'],
                'nome': client['nome'],
                'email': client['email'],
                'beneficio': client['beneficio'],
                'estado_civil': client['estado_civil'],
                'sexo': client['sexo'],
                'nome_mae': client['nome_mae'],
                'nome_pai': client['nome_pai']
            })

def consultar_emprestimos(clientes):
    clientes_com_emprestimo = []
    for client in clientes:
        cpf = client['cpf']
        url = f"{BASE_URL}/emprestimos/clientes/{cpf}/emprestimos/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            emprestimos = response.json()
            if emprestimos:
                for emprestimo in emprestimos:
                    client_data = {
                        'cpf': client['cpf'],
                        'nome': client['nome'],
                        'email': client['email'],
                        'beneficio': client['beneficio'],
                        'estado_civil': client['estado_civil'],
                        'sexo': client['sexo'],
                        'nome_mae': client['nome_mae'],
                        'nome_pai': client['nome_pai'],
                        'emprestimo_id': emprestimo['id'],
                        'valor_solicitado': emprestimo['valor_solicitado'],
                        'taxa_juros': emprestimo['taxa_juros'],
                        'num_parcelas': emprestimo['num_parcelas'],
                        'valor_total': emprestimo['valor_total'],
                        'valor_parcela': emprestimo['valor_parcela']
                    }
                    clientes_com_emprestimo.append(client_data)
        except requests.exceptions.RequestException as e:
            print(f"Erro ao consultar empréstimos para o CPF {cpf}: {e}")
    return clientes_com_emprestimo

def salvar_emprestimos_csv(clientes_com_emprestimo, nome_arquivo):
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['cpf', 'nome', 'email', 'beneficio', 'estado_civil', 'sexo', 'nome_mae', 'nome_pai', 'emprestimo_id', 'valor_solicitado', 'taxa_juros', 'num_parcelas', 'valor_total', 'valor_parcela']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for cliente in clientes_com_emprestimo:
            writer.writerow(cliente)

allClients = get_all_clients()

if allClients:
    salvar_clientes_csv(allClients, 'clientes.csv')
    print("Arquivo CSV com todos os clientes gerado com sucesso!")
    
    clientes_com_emprestimo = consultar_emprestimos(allClients)
    if clientes_com_emprestimo:
        salvar_emprestimos_csv(clientes_com_emprestimo, 'clientes_com_emprestimos.csv')
        print("Arquivo CSV com clientes e seus empréstimos gerado com sucesso!")
    else:
        print("Nenhum cliente com empréstimo encontrado.")
else:
    print("Nenhum cliente encontrado ou erro ao obter clientes.")
