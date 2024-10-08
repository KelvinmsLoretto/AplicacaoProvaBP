import requests
from bs4 import BeautifulSoup

# URLs do site
login_url = "https://www.saucedemo.com/"
inventory_url = "https://www.saucedemo.com/inventory.html"

# Cabeçalhos comuns para simular um navegador real
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": login_url,
    "Content-Type": "application/x-www-form-urlencoded"
}

# Dados de login - credenciais fornecidas
payload = {
    "user-name": "standard_user",
    "password": "secret_sauce"
}

# Função principal para realizar o login e acessar o inventário
def main():
    with requests.Session() as session:
        # Primeiro, visitar a página de login para obter cookies e tokens
        response = session.get(login_url, headers=headers)
        if response.status_code != 200:
            print(f"Erro ao acessar a página de login. Código de status: {response.status_code}")
            return

        # Enviar a requisição de login
        post_login_url = "https://www.saucedemo.com/"  # Endpoint específico para login
        login_response = session.post(post_login_url, headers=headers, data=payload)

        # Verificar se o login foi bem-sucedido
        if login_response.status_code == 200 and "inventory.html" in login_response.text:
            print("Login bem-sucedido! Acessando a página de inventário...")

            # Acessar a página de inventário
            inventory_response = session.get(inventory_url, headers=headers)
            if inventory_response.status_code == 200:
                print("Inventário acessado com sucesso.")
                # Extrair os itens do inventário
                extract_inventory(inventory_response.text)
            else:
                print(f"Erro ao acessar a página de inventário. Código de status: {inventory_response.status_code}")
        else:
            print(f"Falha no login! Código de status: {login_response.status_code}")

# Função para extrair e imprimir itens do inventário
def extract_inventory(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    items = soup.find_all(class_='inventory_item')
    
    if not items:
        print("Nenhum item encontrado no inventário. Pode haver um problema com a autenticação.")
        return

    for item in items:
        nome = item.find(class_='inventory_item_name').get_text(strip=True)
        descricao = item.find(class_='inventory_item_desc').get_text(strip=True)
        preco = item.find(class_='inventory_item_price').get_text(strip=True)
        print(f"Nome: {nome}, Descrição: {descricao}, Preço: {preco}")

if __name__ == "__main__":
    main()