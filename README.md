# Aplicação Prova BP - Sistema Bancário com Web Scraping

Este projeto implementa um sistema bancário Django com funcionalidades de geração de dados, web scraping e importação de produtos. O projeto foi desenvolvido como parte de uma avaliação técnica.

## 📋 Índice

- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Execução das Etapas](#execução-das-etapas)
  - [Etapa 1: Geração de Clientes e Empréstimos](#etapa-1-geração-de-clientes-e-empréstimos)
  - [Etapa 2: Web Scraping](#etapa-2-web-scraping)
  - [Etapa 3: Importação de Produtos](#etapa-3-importação-de-produtos)
  - [Etapa 4: Testes](#etapa-4-testes)
- [Análise de Desempenho](#análise-de-desempenho)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Dificuldades e Soluções](#dificuldades-e-soluções)
- [Melhorias Implementadas](#melhorias-implementadas)

## 🛠️ Requisitos

- Python 3.8+
- Django 4.0+
- Chrome/Chromium (para Selenium)
- ChromeDriver (será baixado automaticamente)

## 📦 Instalação

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd AplicacaoProvaBP
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
```

### 3. Ative o ambiente virtual
**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instale as dependências
    ```bash
pip install -r requirements.txt
```

### 5. Execute as migrações
```bash
python manage.py migrate
```

### 6. Crie um superusuário (para acessar o admin)
    ```bash
python manage.py createsuperuser
```
**Siga as instruções para criar seu usuário e senha.**

## ⚙️ Configuração

### Configurar o banco de dados
O projeto usa SQLite por padrão. Para usar outro banco, edite `ApiBancaria/settings.py`.

### Verificar instalação
```bash
python manage.py check
```

### Testar o servidor Django
    ```bash
python manage.py runserver
```
Acesse http://localhost:8000 para verificar se o Django está funcionando.

## 🚀 Execução das Etapas

### Etapa 1: Geração de Clientes e Empréstimos

**Objetivo:** Gerar 50 clientes com dados fictícios e 1-3 empréstimos por cliente, aprovar automaticamente empréstimos com taxa > 4% e exportar para CSV.

#### Execução:
    ```bash
python scripts/gerar_dados_etapa1.py
```

#### Resultados esperados:
- ✅ 50 clientes gerados com dados realistas
- ✅ 1-3 empréstimos por cliente (total ~100-150 empréstimos)
- ✅ Empréstimos com taxa > 4% aprovados automaticamente
- ✅ Arquivos CSV gerados: `clientes_gerados.csv` e `emprestimos_gerados.csv`

#### Verificação:
```bash
# Verificar arquivos gerados
dir *.csv
# ou no Linux/Mac:
ls *.csv
```

### Etapa 2: Web Scraping

**Objetivo:** Coletar produtos do site https://www.saucedemo.com/ usando dois métodos diferentes (Selenium e Requests), testando todos os usuários disponíveis.

#### 2.1 Web Scraping com Selenium (Recomendado)

```bash
python scripts/webscraping/scrape_selenium.py
```

**Funcionalidades implementadas:**
- ✅ Coleta dinâmica de usuários da interface
- ✅ Coleta dinâmica da senha da interface
- ✅ Testa login com todos os usuários disponíveis
- ✅ Coleta produtos de cada usuário que consegue fazer login
- ✅ Salva no CSV com coluna "username" para identificar origem
- ✅ Tratamento de erros robusto (pula usuários com problemas)
- ✅ Execução headless (sem interface gráfica)

#### 2.2 Web Scraping com Requests (Alternativo)

```bash
python scripts/webscraping/scrape_requests.py
```

**Nota:** Este método pode ter limitações devido ao JavaScript necessário para login.

#### 2.3 Comparação de Desempenho

```bash
python scripts/webscraping/comparar_desempenho.py
```

#### Resultados esperados:
- ✅ Arquivo `products_selenium.csv` com produtos coletados
- ✅ Arquivo `products_requests.csv` (se funcionar)
- ✅ Arquivo `performance_comparison.txt` com comparação de tempos
- ✅ Coluna "username" no CSV para identificar origem dos dados

### Etapa 3: Importação de Produtos

**Objetivo:** Importar os produtos coletados para o banco de dados Django.

#### 3.1 Executar script de importação

```bash
python scripts/import_scraped_products.py
```

#### 3.2 Verificar dados importados

```bash
# Acessar o Django admin
python manage.py runserver
```

Acesse http://localhost:8000/admin e faça login com as credenciais que você criou durante o `createsuperuser`.

**Nota:** Se você ainda não criou um superusuário, execute:
```bash
python manage.py createsuperuser
```

#### 3.3 Verificar via shell Django

```bash
python manage.py shell
```

```python
from products_scraped.models import ProductScraped
print(f"Total de produtos: {ProductScraped.objects.count()}")
print(f"Produtos por fonte: {ProductScraped.objects.values('fonte').distinct()}")
```

### Etapa 4: Testes

#### 4.1 Executar todos os testes

```bash
python manage.py test
```

#### 4.2 Testes específicos

```bash
# Testes do modelo ProductScraped
python manage.py test products_scraped.tests

# Testes do script de importação
python scripts/test_import_script.py
```

## 📊 Análise de Desempenho

### Comparação Selenium vs Requests

| Método | Vantagens | Desvantagens | Tempo Médio |
|--------|-----------|--------------|-------------|
| **Selenium** | ✅ Suporte completo a JavaScript<br>✅ Interação com elementos dinâmicos<br>✅ Coleta credenciais da interface<br>✅ Tratamento robusto de erros | ⚠️ Mais lento<br>⚠️ Requer ChromeDriver | ~30-45 segundos |
| **Requests** | ✅ Mais rápido<br>✅ Menos recursos | ❌ Limitações com JavaScript<br>❌ Pode não funcionar em sites dinâmicos | ~5-10 segundos |

### Resultados Esperados

**Selenium:**
- ✅ Coleta todos os usuários da interface
- ✅ Coleta senha dinamicamente
- ✅ Testa todos os usuários
- ✅ Coleta produtos de usuários válidos
- ✅ Salva com identificação de usuário

**Requests:**
- ⚠️ Pode falhar devido ao JavaScript
- ⚠️ Pode não conseguir fazer login
- ⚠️ Pode não coletar produtos

## 📁 Estrutura do Projeto

```
AplicacaoProvaBP/
├── ApiBancaria/                 # Configurações Django
├── apps/
│   ├── clientes/               # App de clientes
│   ├── emprestimos/            # App de empréstimos
│   └── products_scraped/       # App para produtos coletados
├── scripts/
│   ├── gerar_dados_etapa1.py   # Geração de dados
│   ├── webscraping/
│   │   ├── scrape_selenium.py  # Web scraping com Selenium
│   │   ├── scrape_requests.py  # Web scraping com Requests
│   │   └── comparar_desempenho.py
│   ├── import_scraped_products.py
│   └── test_import_script.py
├── *.csv                       # Arquivos de dados gerados
└── README.md
```

## 🔧 Dificuldades e Soluções

### 1. Coleta Dinâmica de Credenciais

**Problema:** Como coletar usuários e senhas da interface sem hardcoding?

**Solução:** Implementei múltiplas estratégias:
- ✅ Parse da seção `login_credentials`
- ✅ Busca por elementos específicos
- ✅ Fallback para valores conhecidos
- ✅ Tratamento robusto de erros

### 2. Tratamento de Erros por Usuário

**Problema:** Script parava quando um usuário falhava no login.

**Solução:** Implementei tratamento de exceções que:
- ✅ Captura erros específicos por usuário
- ✅ Continua para o próximo usuário
- ✅ Registra falhas sem interromper execução
- ✅ Coleta dados de usuários que funcionam

### 3. Identificação de Origem dos Dados

**Problema:** Como identificar de qual usuário veio cada produto?

**Solução:** Adicionei coluna "username" no CSV:
- ✅ Primeira coluna identifica o usuário
- ✅ Permite análise por usuário
- ✅ Facilita debugging e validação

### 4. Compatibilidade com Diferentes Ambientes

**Problema:** Scripts não funcionavam em diferentes sistemas.

**Solução:** Implementei:
- ✅ Configuração headless para Selenium
- ✅ Fallbacks para diferentes cenários
- ✅ Tratamento de encoding
- ✅ Logs detalhados para debugging

## 🚀 Melhorias Implementadas

### 1. Coleta Inteligente de Credenciais
- ✅ Detecta automaticamente usuários disponíveis
- ✅ Coleta senha dinamicamente da interface
- ✅ Múltiplas estratégias de fallback
- ✅ Logs detalhados do processo

### 2. Processamento Robusto
- ✅ Testa todos os usuários disponíveis
- ✅ Coleta produtos de cada usuário válido
- ✅ Tratamento de erros por usuário
- ✅ Continuação automática após falhas

### 3. Dados Estruturados
- ✅ CSV com identificação de usuário
- ✅ Separação clara de dados por origem
- ✅ Facilita análise e debugging
- ✅ Compatível com importação posterior

### 4. Comparação de Métodos
- ✅ Script de comparação de desempenho
- ✅ Análise de tempo de execução
- ✅ Relatório detalhado de diferenças
- ✅ Documentação de limitações

## 🔍 Verificação de Funcionamento

### Checklist de Verificação

Após executar todas as etapas, verifique:

- [ ] `clientes_gerados.csv` e `emprestimos_gerados.csv` existem
- [ ] `products_selenium.csv` contém produtos com coluna "username"
- [ ] `performance_comparison.txt` foi gerado
- [ ] Produtos foram importados no banco de dados
- [ ] Testes passam sem erros

### Comandos de Verificação

```bash
# Verificar arquivos gerados
dir *.csv *.txt

# Verificar dados no banco
python manage.py shell
>>> from products_scraped.models import ProductScraped
>>> print(f"Produtos importados: {ProductScraped.objects.count()}")

# Executar testes
python manage.py test
```

## 📝 Notas Importantes

1. **ChromeDriver:** O Selenium baixará automaticamente o ChromeDriver compatível
2. **Execução Headless:** Os scripts rodam sem interface gráfica para melhor performance
3. **Tratamento de Erros:** O sistema continua funcionando mesmo se alguns usuários falharem
4. **Dados Realistas:** Os dados gerados usam Faker para criar informações realistas
5. **Compatibilidade:** Testado em Windows, Linux e Mac

## 🤝 Contribuição

Para contribuir com melhorias:

1. Teste todas as etapas em seu ambiente
2. Documente qualquer problema encontrado
3. Proponha melhorias com exemplos práticos
4. Mantenha a compatibilidade com diferentes sistemas

---

**Desenvolvido como parte da avaliação técnica BP - 2024**

