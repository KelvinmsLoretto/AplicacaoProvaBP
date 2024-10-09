import requests
import csv
import time
import json
import re

def export_data():
    login_url = 'https://www.saucedemo.com/'
    inventory_url = 'https://www.saucedemo.com/static/js/main.018d2d1e.chunk.js'
    login_payload = {
        'user-name': 'standard_user',
        'password': 'secret_sauce'
    }

    with requests.Session() as session:
        start_time = time.time()

        session.post(login_url, data=login_payload)

        response = session.get(inventory_url)

        content = response.text
        if content:
            parts = content.split('D=[')
            extracted_data = []
            for part in parts[1:]:
                parted_json = part.split(']')[0]
                items = parted_json.split('},')
                for item in items:
                    item = item.replace("}", "") + '}'
                    item = re.sub(r'(\w+):', r'"\1":', item)
                    item_dict = json.loads(item)

                    extracted_data.append({
                    'nome': item_dict['name'],
                    'descricao': item_dict['desc'],
                    'preco': item_dict['price']
                    })

                with open('produtos_request.csv', mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=['nome', 'descricao', 'preco', 'image_url'])
                    writer.writeheader()
                    writer.writerows(extracted_data)

            end_time = time.time()
            execution_time = end_time - start_time

            print("Dados dos produtos salvos em 'produtos_request.csv'")
            print(f"Tempo de execução: {execution_time:.2f} segundos")
        else:
            print("Nenhum conteúdo encontrado na resposta.")

if __name__ == "__main__":
    export_data()
