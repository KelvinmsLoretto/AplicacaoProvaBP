# Teste BP Programador

## Início Rápido

1. **Dar um Fork do Repositório:**

2. **Criar uma Nova Branch (com seu nome):**
    ```bash
    git checkout -b nome-do-participante

3. **Fazer as Alterações e Commit:**

    *Realizar as modificações necessárias, e depois fazer commit das alterações:*
    ```bash
        git add .
        git commit -m "Descrição das alterações feitas"
4. **Push da Nova Branch para o Fork:**

    *Fazer o push da branch criada para o repositório forked:*
    ```bash
    git push origin nome-do-participante

5. **Criar um Pull Request:**

    *Após o push, o participante deve ir até o repositório original no GitHub e criar um pull request a partir da sua branch recém-criada. No pull request, eles devem descrever as alterações que fizeram e a finalidade do PR.*

## Para migrar os cliente pré criado
**Importar clientes: Após iniciar o Django, execute o comando:**
    ```bash
    python manage.py importar_clientes

## Etapas da prova

### Etapa 1: Manipulação de Clientes e Empréstimos
*1.1 Identificar clientes e gerar empréstimos para eles.
1.2 Cadastrar 50 novos clientes (use a biblioteca Faker para gerar dados falsos).
1.3 Incluir novos empréstimos para esses clientes com valores e taxas de juros variados.
1.4 Aprovar empréstimos com taxas superiores a 4%.
1.5 Exportar todos os dados de clientes e empréstimos para um arquivo CSV.
Etapa 2: Web Scraping
2.1 Realizar web scraping da página https://www.saucedemo.com/
2.2.1 Coletar todas os prudtos listadas e retornar em um arquivo CSV.
2.3.2 Comparar o desempenho entre o uso de Selenium e Requests (opcional e diferencial).*

### Etapa 3: Criar um app para receber os dados removido do site:
3.1 Iniciar um novo app no django com a finalidade de guardar dados retirados da pagina saucedemo
3.2 fazer a importação dos dados (mostrar script usado)
3.3 testar o app

### Etapa 4: Relatório final
*Modificar essa etapa no seu README.md trazendo os dados do desempenho selenium e requests caso tenha feito.*
Escreve quais foram as dificuldades e ponntos avistados (Obrigatório)


**Sinta-se à vontade para contribuir e adicionar mais funcionalidades caso necessario!**