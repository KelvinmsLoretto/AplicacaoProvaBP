# Aplicação Prova BP

## Início Rápido

1. **Dar um Fork do Repositório**

2. **Criar uma Nova Branch (com seu nome):**
    ```bash
    git checkout -b nome-do-participante
    ```

3. **Fazer as Alterações e Commit:**

    _Realizar as modificações necessárias e depois fazer commit das alterações:_
    ```bash
    git add .
    git commit -m "Descrição das alterações feitas"
    ```

4. **Push da Nova Branch para o Fork:**

    _Fazer o push da branch criada para o repositório forked:_
    ```bash
    git push origin nome-do-participante
    ```

5. **Criar um Pull Request:**

    _Após o push, o participante deve ir até o repositório original no GitHub e criar um pull request a partir da sua branch recém-criada. No pull request, devem descrever as alterações que fizeram e a finalidade do PR._

## Importar Clientes

1. **Para importar os clientes pré-cadastrados:**
    ```bash
    python manage.py importar_clientes
    ```

## Etapas da Prova

### Etapa 1: Manipulação de Clientes e Empréstimos

1.1 Identificar clientes e gerar empréstimos para eles.<br>
1.2 Cadastrar 50 novos clientes (use a biblioteca Faker para gerar dados falsos).<br>
1.3 Incluir novos empréstimos para esses clientes com valores e taxas de juros variados.<br>
1.4 Aprovar empréstimos com taxas superiores a 4%.<br>
1.5 Exportar todos os dados de clientes e empréstimos para um arquivo CSV.<br>

### Etapa 2: Web Scraping

2.1 Realizar web scraping da página [https://www.saucedemo.com/](https://www.saucedemo.com/)<br>
2.2.1 Coletar todos os produtos listados e retornar em um arquivo CSV.<br>
2.2.2 Comparar o desempenho entre o uso de Selenium e Requests (opcional e diferencial).<br>

### Etapa 3: Criar um App para Receber os Dados Removidos do Site

3.1 Iniciar um novo app no Django com a finalidade de guardar dados retirados da página [https://www.saucedemo.com/](https://www.saucedemo.com/)<br>
3.2 Fazer a importação dos dados (mostrar script usado)<br>
3.3 Escrever testes para o app<br>

### Etapa 4: Relatório Final

**Relatório sobre a Aplicação Prova BP**

Ao desenvolver a **Aplicação Prova BP**, tomei diversas decisões técnicas que visaram otimizar a eficiência, a escalabilidade e a robustez da aplicação. Este relatório detalha as escolhas feitas, os insights obtidos durante o processo e os desafios enfrentados, especialmente relacionados ao uso de bibliotecas para web scraping.

#### 1. Escolha do Framework Django

Optar pelo **Django** como framework principal foi uma decisão estratégica baseada na necessidade de desenvolver uma aplicação web robusta e escalável de forma rápida e eficiente. Django oferece uma arquitetura bem estruturada, ORM poderoso para interação com o banco de dados, e um painel administrativo integrado que facilita o gerenciamento de clientes, empréstimos e produtos.

#### 2. Uso do Selenium para Web Scraping

Durante a implementação da Etapa 2: Web Scraping, inicialmente considerei o uso da biblioteca `requests` para coletar dados da página [https://www.saucedemo.com/](https://www.saucedemo.com/). No entanto, enfrentei várias limitações:

- **Carregamento Dinâmico de Conteúdo:** Muitos elementos da página eram carregados via JavaScript, o que não é manipulado pelo `requests`, que apenas realiza requisições HTTP estáticas.
  
- **Simulação de Interações Humanas:** A necessidade de interagir com elementos dinâmicos, como cliques e preenchimento de formulários, era complexa com `requests`.

Esses desafios poderiam comprometer a eficácia do scraping, resultando em dados incompletos ou incorretos, o que, em um cenário real, poderia acabar com o produto devido à falta de confiabilidade dos dados coletados.

**Insight e Decisão:**  
Percebendo essas limitações, decidi utilizar o **Selenium**, que permite controlar um navegador de forma programática. O Selenium lida eficientemente com páginas dinâmicas, executa JavaScript, e simula interações humanas com precisão. Isso simplificou o processo de coleta de dados, garantindo que todos os elementos fossem acessíveis e manipulados corretamente.

#### 3. Problemas com a Biblioteca Requests

Durante a tentativa de implementar o scraping com `requests`, encontrei um erro crítico:

*django.db.utils.IntegrityError: NOT NULL constraint failed: emprestimos_emprestimo.id*

Esse erro indicava que o campo `id` do modelo `Emprestimo` estava recebendo valores inesperados, possivelmente relacionados à incompatibilidade entre os tipos de dados utilizados. Além disso, o `requests` não conseguia lidar com o conteúdo dinâmico da página, resultando em falhas na coleta de dados.

**Impacto:**  
Tais erros não apenas interrompem o fluxo de trabalho, mas também podem comprometer a integridade dos dados e a estabilidade do produto, tornando-o inutilizável ou gerando informações erradas para análises futuras.

#### 4. Estrutura do Aplicativo e Organização das Pastas

A aplicação foi organizada de forma modular, dividindo funcionalidades em diferentes aplicativos dentro do projeto Django. A seguir, uma descrição detalhada de cada parte do aplicativo e o conteúdo de suas respectivas pastas:

AplicacaoProvaBP/
├── apps/
│   ├── clientes/
│   │   ├── migrations/
│   │   ├── management/
│   │   │   └── commands/
│   │   │       ├── gerar_clientes.py
│   │   │       └── exportar_clientes_emprestimos.py
│   │   ├── models.py
│   │   ├── admin.py
│   │   └── views.py
│   ├── emprestimos/
│   │   ├── migrations/
│   │   ├── management/
│   │   │   └── commands/
│   │   │       ├── gerar_emprestimos.py
│   │   │       ├── aprovar_emprestimos.py
│   │   ├── models.py
│   │   ├── admin.py
│   │   └── views.py
│   ├── produtos/
│   │   ├── migrations/
│   │   ├── management/
│   │   │   └── commands/
│   │   │       ├── gerar_produtos.py
│   │   │       └── import_products.py
│   │   ├── models.py
│   │   ├── admin.py
│   │   └── views.py
│   ├── scripts/
│   │   ├── selenium_scraping.py
│   │   └── requests_scraping.py
│   ├── data/
│   │   ├── produtos.csv
│   │   └── clientes_emprestimos.csv
├── AplicacaoProvaBP/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── README.md


**Descrição das Pastas e Arquivos**

##### **Clientes**

- **models.py:** Define o modelo `Cliente`, representando os clientes da aplicação com atributos como nome, email, telefone, etc.
- **admin.py:** Configurações para o painel de administração do Django, permitindo gerenciar clientes facilmente.
- **management/commands/gerar_clientes.py:** Comando personalizado para gerar dados de clientes automaticamente, facilitando testes e desenvolvimento.
- **management/commands/exportar_clientes_emprestimos.py:** Comando para exportar dados de clientes e seus empréstimos para um arquivo CSV, permitindo análises externas.

##### **Empréstimos**

- **models.py:** Define o modelo `Emprestimo`, representando os empréstimos associados aos clientes, com campos como valor solicitado, taxa de juros, número de parcelas, etc.
- **admin.py:** Configurações para o painel de administração do Django, permitindo gerenciar empréstimos de forma eficiente.
- **management/commands/gerar_emprestimos.py:** Comando personalizado para gerar dados de empréstimos automaticamente.
- **management/commands/aprovar_emprestimos.py:** Comando para aprovar automaticamente empréstimos com base em critérios predefinidos, como taxa de juros.

##### **Produtos**

- **models.py:** Define o modelo `Product`, representando os produtos coletados da página [https://www.saucedemo.com/](https://www.saucedemo.com/), com atributos como nome, preço, descrição, etc.
- **admin.py:** Configurações para o painel de administração do Django, permitindo gerenciar produtos facilmente.
- **management/commands/gerar_produtos.py:** Comando personalizado para gerar dados de produtos automaticamente, facilitando testes e desenvolvimento.
- **management/commands/import_products.py:** Comando personalizado para importar produtos a partir de um arquivo CSV.

##### **Scripts**

- **selenium_scraping.py:** Script responsável por realizar o web scraping utilizando Selenium, coletando dados dinâmicos da página [https://www.saucedemo.com/](https://www.saucedemo.com/) e salvando-os em arquivos CSV na pasta `data/`.
- **requests_scraping.py:** Script responsável por realizar o web scraping utilizando a biblioteca Requests. Este script serve como referência para comparar o desempenho e a eficiência em relação ao Selenium.

##### **Data**

- **produtos_selenium.csv:** Arquivo CSV gerado pelo script de web scraping que contém todos os produtos coletados da página.
- **clientes_emprestimos.csv:** Arquivo CSV gerado pelo comando de exportação, contendo dados de clientes e seus respectivos empréstimos.

##### **Pastas Principais**

- **AplicacaoProvaBP/:** Diretório principal do projeto Django, contendo configurações globais como `settings.py`, `urls.py` e `wsgi.py`.
- **migrations/:** Pastas dentro de cada aplicativo que armazenam os arquivos de migração do banco de dados, garantindo versionamento e consistência dos dados.
- **management/commands/:** Diretório para comandos personalizados do Django, permitindo a execução de tarefas específicas via `manage.py`.
- **scripts/:** Contém scripts auxiliares para funcionalidades como web scraping, separados dos aplicativos principais para melhor organização.
- **data/:** Pasta destinada a armazenar arquivos de dados gerados pelos scripts e comandos da aplicação.
- **requirements.txt:** Lista de dependências Python necessárias para rodar a aplicação, facilitando a instalação em novos ambientes.
- **README.md:** Este arquivo, fornecendo uma visão geral detalhada do projeto.

## 🔧 Comandos Necessários para Rodar a Aplicação

Para facilitar a configuração e execução da aplicação, abaixo estão os comandos essenciais:

1. **Clonar o Repositório:**
    ```bash
    git clone https://github.com/seu-usuario/AplicacaoProvaBP.git
    cd AplicacaoProvaBP
    ```

2. **Criar e Ativar um Ambiente Virtual (Recomendado):**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Instalar Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Aplicar Migrações:**
    ```bash
    python manage.py migrate
    ```

5. **Criar Superusuário:**
    ```bash
    python manage.py createsuperuser
    ```

6. **Gerar Dados de Clientes:**
    ```bash
    python manage.py gerar_clientes
    ```

7. **Gerar Dados de Empréstimos:**
    ```bash
    python manage.py gerar_emprestimos
    ```

8. **Aprovar Empréstimos com Taxa de Juros > 4%:**
    ```bash
    python manage.py aprovar_emprestimos
    ```

9. **Importar Produtos a partir de um CSV:**
    - **Criar o Arquivo CSV:**

        Você pode usar o arquivo de exemplo fornecido ou criar o seu próprio. Salve o conteúdo abaixo em um arquivo chamado `produtos_selenium.csv` na pasta `data/`:

        ```csv
        Nome do Produto,Descrição,Preço
        Sauce Labs Backpack,"carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.",$29.99
        Sauce Labs Bike Light,"A red light isn't the desired state in testing but it sure helps when riding your bike at night. Water-resistant with 3 lighting modes, 1 AAA battery included.",$9.99
        Sauce Labs Bolt T-Shirt,"Get your testing superhero on with the Sauce Labs bolt T-shirt. From American Apparel, 100% ringspun combed cotton, heather gray with red bolt.",$15.99
        Sauce Labs Fleece Jacket,It's not every day that you come across a midweight quarter-zip fleece jacket capable of handling everything from a relaxing day outdoors to a busy day at the office.,$49.99
        Sauce Labs Onesie,"Rib snap infant onesie for the junior automation engineer in development. Reinforced 3-snap bottom closure, two-needle hemmed sleeved and bottom won't unravel.",$7.99
        Test.allTheThings() T-Shirt (Red),"This classic Sauce Labs t-shirt is perfect to wear when cozying up to your keyboard to automate a few tests. Super-soft and comfy ringspun combed cotton.",$15.99
        ```

    - **Executar o Comando de Importação:**
        ```bash
        python manage.py import_products data/produtos_selenium.csv
        ```

10. **Exportar Dados para CSV:**
    ```bash
    python manage.py exportar_clientes_emprestimos
    ```

11. **Executar o Web Scraping com Selenium:**

    Certifique-se de que o WebDriver correspondente ao seu navegador (por exemplo, GeckoDriver para Firefox ou ChromeDriver para Chrome) está instalado e configurado no seu `PATH`.

    ```bash
    python scripts/selenium_scraping.py
    ```

12. **Executar o Web Scraping com Requests (Opcional):**
    ```bash
    python scripts/requests_scraping.py
    ```

13. **Iniciar o Servidor de Desenvolvimento:**
    ```bash
    python manage.py runserver
    ```

    Acesse a aplicação em [http://localhost:8000/](http://localhost:8000/) e o painel de administração em [http://localhost:8000/admin/](http://localhost:8000/admin/).


## 📚 Considerações Finais

A **Aplicação Prova BP** é uma solução robusta para o gerenciamento de clientes, empréstimos e produtos, combinando a eficiência do Django com a flexibilidade do Selenium para automação de tarefas complexas. As escolhas técnicas feitas durante o desenvolvimento, como a utilização de `UUIDField` e o Selenium, foram fundamentais para garantir a confiabilidade e a escalabilidade da aplicação.

**Destaques:**

- **Estrutura Modular:** Facilitando a manutenção e futuras expansões.
- **Automação Eficiente:** Com comandos personalizados que agilizam processos como geração e aprovação de empréstimos.
- **Exportação de Dados:** Permitindo análises externas e integrações com outras ferramentas.
- **Web Scraping Avançado:** Utilizando Selenium para coleta confiável de dados dinâmicos.

**Próximos Passos:**

- **Implementação de Funcionalidades Adicionais:** Como autenticação de usuários e relatórios mais detalhados.
- **Melhoria na Interface do Usuário:** Tornando a aplicação mais intuitiva e amigável.
- **Monitoramento e Logging:** Para acompanhar o desempenho da aplicação e identificar rapidamente quaisquer problemas.

Estou satisfeito com os resultados alcançados e confiante de que esta aplicação atende às necessidades propostas de forma eficiente e eficaz. Continuarei aprimorando e adicionando novas funcionalidades conforme necessário, sempre buscando as melhores práticas e soluções tecnológicas.


----
