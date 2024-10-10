
## Relatório do Projeto

## Credenciais de acesso ao app

- login: standart_user
- senha: secret_sauce

Este projeto tem como objetivo simular a geração de clientes e empréstimos, além de realizar scraping de produtos e seus respectivos preços. Foi desenvolvido utilizando o framework Django e integra todas as operações em um ambiente web acessível. Cada etapa do desenvolvimento envolveu desafios únicos, como a integração com banco de dados, web scraping e a adaptação ao Django, visto que o framework era uma novidade no início do projeto.

## Tecnologias Utilizadas

- **Python**: Linguagem principal utilizada para a implementação.
- **Django**: Framework web utilizado para gerenciar o back-end da aplicação.
- **Selenium**: Utilizado para realizar o web scraping.
- **Faker**: Biblioteca utilizada para a geração de dados fictícios.
- **CSV**: Formato utilizado para o salvamento de dados temporários durante as primeiras iterações.

## Funcionalidades Implementadas

1. **Geração de Clientes**:
   - Utiliza a biblioteca `Faker` para gerar dados fictícios.
   - Dados salvos no banco de dados do Django, com campos customizados nos `models.py`.

2. **Simulação de Empréstimos**:
   - Criação de empréstimos fictícios com base em regras de aprovação.
   - Aplicação de taxas de juros superiores a 4% para empréstimos aprovados.

3. **Web Scraping de Produtos**:
   - O scraping coleta informações de produtos e preços, utilizando `Selenium`.
   - Os dados são integrados ao banco de dados para posterior visualização no app.

4. **Administração via Django Admin**:
   - Interface de administração gerada automaticamente para gerenciar clientes e empréstimos.
   - Visualização e manipulação de dados de forma facilitada via Django Admin.

## Principais Desafios

- **Familiarização com o Django**: Inicialmente, foi necessário estudar as funcionalidades e realizar configurações no `Visual Studio Code` para integrar o Python e o framework de maneira adequada.
- **Geração de Dados**: Houve dificuldades com a instalação e uso da biblioteca `Faker`, pois não havia familiaridade com o `pip`.
- **Web Scraping**: A implementação de scraping foi a parte mais desafiadora, exigindo extensas pesquisas e tentativas para configurar o `Selenium`.
- **Erro 404 no Navegador**: Um dos principais erros enfrentados foi ao tentar acessar o app, o que estava relacionado à falta de integração adequada entre os dados CSV e o banco de dados do Django.
- **Refatoração do Código**: A refatoração do código de geração de clientes e empréstimos para adequá-lo às estruturas do Django foi crucial para a integração correta com o banco de dados.

## Conclusão

O desenvolvimento deste projeto foi uma experiência intensa de aprendizado, tanto em termos de novas ferramentas quanto em relação à resolução de problemas em tempo real. Cada desafio encontrado proporcionou novas habilidades e a capacidade de pensar de maneira crítica sobre cada etapa do desenvolvimento.
