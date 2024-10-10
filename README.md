
## Etapa 1 - Clientes e Empréstimos

Veja o guia resumido de comandos no final deste pull request.

- **Cadastro de Clientes**: Implementação de um comando utilizando a biblioteca Faker para gerar dados fictícios de clientes, facilitando o desenvolvimento e os testes.
- **Aprovação Automática de Empréstimos**: Empréstimos com taxas de juros superiores a 4% são aprovados automaticamente.
- **Exportação de Dados**: Implementação de funcionalidades para exportar dados de clientes e empréstimos para arquivos CSV, permitindo análises externas.

Para executar os comandos, use: `python manage.py nome_do_comando`

---

## Etapa 2 - Extração de Dados com Requests e Selenium

Nesta etapa, foram criados dois scripts para extração de dados com abordagens diferentes:

- **Selenium**: Utilizado para uma extração mais "amigável", permitindo visualizar o processo. Embora seja mais lento, o Selenium é vantajoso para páginas com carregamento dinâmico.
- **Requests**: Mais performático, porém menos flexível. Ideal para extração direta de dados sem necessidade de interação visual.

### Resultados de Performance

| Método        | Tempo (dentro do projeto) | Tempo (fora do projeto) |
|---------------|---------------------------|--------------------------|
| Selenium      | 3.16 segundos             | 1.7 segundos             |
| Requests      | 0.81 segundos             | 0.30 segundos            |

Para executar os scripts, use: `python nome_do_arquivo.py`

---

## Etapa 3 - Desenvolvimento de Nova Rota para Produtos, Importação de Dados e Testes Unitários

- **CRUD para Produtos**: Desenvolvimento de um CRUD padrão para gerenciar registros de produtos.
- **Importação de Dados**: Criação de uma rota para importar dados diretamente do site para o banco de dados, utilizando o script desenvolvido na etapa anterior.
- **Testes Unitários**: Implementação de testes para garantir a integridade e funcionalidade do CRUD de produtos.

Para rodar o servidor, utilize: `python manage.py runserver 8080` e acesse o Swagger para documentação das APIs.

---

## Dificuldades

O principal desafio durante o desenvolvimento foi a extração de dados via Requests na segunda etapa, devido à natureza dinâmica do HTML utilizado. Foi necessário explorar diferentes abordagens para capturar os valores corretamente.

Além disso, houve um problema nos endpoints de criação e simulação de empréstimos em que CPFs iniciados em "0" eram tratados como inteiros, o que causava erros. A solução foi ajustar o tipo dos parâmetros no request.

---

## Guia de Execução dos Comandos

### 0. Configuração Inicial

1. **Zerar a base de dados**: `rm .\db.sqlite3`
2. **Aplicar migrações**: `python manage.py migrate`
3. **Importar clientes padrão**: `python manage.py importar_clientes`

### 1. Gerenciamento de Clientes e Empréstimos

1. **Iniciar o servidor**: `python manage.py runserver 8080`
2. **Gerar empréstimos com valores aleatórios**: `python manage.py gerar_emprestimos`
3. **Gerar empréstimos prontos para aprovação**: `python manage.py gerar_emprestimos`
4. **Criar novos clientes**: `python manage.py criar_clientes`
5. **Aprovar empréstimos com juros acima de 4%**: `python manage.py aprovar_emprestimos`
6. **Exportar dados para CSV**: `python manage.py exportar_dados_csv`

### 2. Extração de Dados

1. **Extrair dados com Requests**: `python manage.py export_data_request`
2. **Extrair dados com Selenium**: `python manage.py export_data_selenium`

### 3. Rotas Disponíveis e Templates JSON

As rotas para gerenciamento de produtos estão disponíveis via `apps.produtos.views.ProdutoViewSet`.

| Ação                      | Método | URL                                          |
|---------------------------|--------|----------------------------------------------|
| Buscar todos os produtos  | GET    | `http://127.0.0.1:8080/api/v1/produtos/produtos` |
| Criar um produto          | POST   | `http://127.0.0.1:8080/api/v1/produtos/produto/create` |
| Atualizar um produto      | PUT    | `http://127.0.0.1:8080/api/v1/produtos/produto/update/<id>` |
| Deletar um produto        | DELETE | `http://127.0.0.1:8080/api/v1/produtos/produto/delete/<id>` |
| Importar produtos de Saucedemo | POST | `http://127.0.0.1:8080/api/v1/produtos/produtos/importar` |
| export todos produtos para um csv | POST | `http://127.0.0.1:8080/api/v1produtos/exportar-produtos-csv/` |

Essas funcionalidades foram implementadas para melhorar o fluxo de desenvolvimento e permitir uma maior flexibilidade na manipulação dos dados.
`{
  "nome": "string",
  "descricao": "string",
  "preco": "string"
} JSON template para produtos`
