# Aplicaçõo Prova BP


## Início Rápido

1. **Dar um Fork do Repositório**

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

## Importar Clientes

1. **para importar os clientes pré cadastrados:**
    ```bash
    python manage.py importar_clientes

## Etapas da prova

### Etapa 1: Manipulação de Clientes e Empréstimos
1.1 Identificar clientes e gerar empréstimos para eles.<br>

 Para gerar empréstimos, você pode usar o comando '  python cria_aprova_emprestimos.py ', executando ele no terminal na raiz do projeto ele vai consultar, gerar e aprovar emprestimos conforme sua escolha para todos clientes cadastrados no banco de dados.

1.2 Cadastrar 50 novos clientes (use a biblioteca Faker para gerar dados falsos).<br>

 Para gerar novos cadastros, você pode usar o comando '  python criar_usuarios.py ', executando ele no terminal na raiz do projeto ele vai criar  novos clientes e salvar no banco de dados conforme você escolher.

1.3 Incluir novos empréstimos para esses clientes com valores e taxas de juros variados.<br>

 Para gerar empréstimos, você pode usar o comando '  python cria_aprova_emprestimos.py ', executando ele no terminal na raiz do projeto ele vai consultar, gerar e aprovar emprestimos conforme sua escolha para todos clientes cadastrados no banco de dados.

1.4 Aprovar empréstimos com taxas superiores a 4%.<br>
    
 Para gerar empréstimos, você pode usar o comando '  python cria_aprova_emprestimos.py ', executando ele no terminal na raiz do projeto ele vai consultar, gerar e aprovar emprestimos conforme sua escolha para todos clientes cadastrados no banco de dados.

1.5 Exportar todos os dados de clientes e empréstimos para um arquivo CSV.<br>

    Para gerar um arquivo csv, você pode usar o comando ' python exportCSV.py ', executando ele no terminal na raiz do projeto ele vai gerar um CSV para todos Clientes e outro CSV com todos emprestimos.


### Etapa 2: Web Scraping
2.1 Realizar web scraping da página [https://www.saucedemo.com/](https://www.saucedemo.com/)<br>

2.2.1 Coletar todas os produtos listadas e retornar em um arquivo CSV.<br>

Para gerar um arquivo csv, você pode usar o comando ' python WebScraping.py ' para o Selenium ou ' python WebScrapingRequest.py ' para requests, executando ele no terminal na raiz do projeto ele vai gerar um CSV com todos os produtos da Saucedemo.

2.3.2 Comparar o desempenho entre o uso de Selenium e Requests (opcional e diferencial).<br>
    Tempo utilizando o Selenium: 2.3280816078186035 segundos
    Tempo utilizando o 0.14171719551086426 segundos


### Etapa 3: Criar um app para receber os dados removido do site:
3.1 Iniciar um novo app no django com a finalidade de guardar dados retirados da pagina [https://www.saucedemo.com/](https://www.saucedemo.com/)<br>
3.2 fazer a importação dos dados (mostrar script usado)<br>
3.3 escrever testes para o app<br>
    Infelizmente, não foi possível criar o app usando as configurações locais sem modificar a estrutura da pasta app ou ApiBancaria, conforme especificado no enunciado da prova. Isso exigiria mais tempo para uma análise detalhada do projeto. Decidi enviar o pull request para não atrasar a entrega e ser o último a entregar. Devido a essas dificuldades, também não foi possível criar os testes para o app.




### Etapa 4: Relatório final
*Modificar essa etapa no seu README.md trazendo os dados do desempenho selenium e requests caso tenha feito.*<br>
Escreve quais foram as dificuldades e ponntos avistados (obrigatório)<br>

Sobre o relatório, foram criados scripts automatizados da forma mais simples possível, a fim de gerar programas executáveis e de fácil manutenção. A maior dificuldade foi importar as configurações do projeto dentro de um novo app sem alterar a pasta app ou ApiBancaria. Esse problema requeria mais tempo para ser resolvido e, para não atrasar a entrega, decidi enviar o pull request mesmo com essas limitações. 


**Sinta-se à vontade para contribuir e adicionar mais funcionalidades caso necessario!**

## Da Avaliação
A prova técnica de TI será avaliada considerando dois principais critérios: qualidade do código e tempo de entrega. O participante deve equilibrar ambos os aspectos, pois a entrega rápida, por si só, não garante uma boa avaliação sem uma codificação robusta e bem estruturada.

A partir de hoje, dia 04/10/2024, o participante tem até 11/10/2024 para concluir e entregar a prova. No entanto, é importante ressaltar que a velocidade da entrega impactará diretamente na avaliação final. Ou seja, embora seja necessário respeitar o prazo, entregar antes do limite pode ser um diferencial positivo, desde que a qualidade do código não seja comprometida. O objetivo é avaliar como o candidato consegue balancear esses dois fatores.

Regras importantes para a entrega:

Não é permitido alterar os apps Django já existentes no projeto fornecido. O participante deve apenas acrescentar as funcionalidades necessárias para cumprir os requisitos da prova.

Todos os scripts utilizados durante o desenvolvimento, como automações, ferramentas de teste ou outros utilitários, devem ser mantidos no repositório para análise e futura execução.

O participante deve entregar um relatório detalhado sobre o desenvolvimento, explicando as decisões tomadas, os desafios enfrentados e as soluções aplicadas. Esse relatório deverá estar presente no projeto e será parte da avaliação final.

Dessa forma, espera-se que o participante demonstre sua habilidade técnica e de gestão de tempo, entregando um projeto de alta qualidade dentro do prazo estipulado.

