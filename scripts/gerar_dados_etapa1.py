#!/usr/bin/env python
"""
Script para gerar dados da Etapa 1 - Manipulação de Clientes e Empréstimos
Gera 50 clientes com Faker e cria 1-3 empréstimos para cada cliente.
Aprova automaticamente empréstimos com taxa de juros > 4%.
Exporta dados para CSV.
"""

import os
import sys
import django
import random
import pandas as pd
from decimal import Decimal
from datetime import datetime

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ApiBancaria.settings')
django.setup()

from faker import Faker
from apps.clientes.models import Cliente, DadosPessoais, ContaBancaria
from apps.emprestimos.models import Emprestimo

# Configurar Faker para dados brasileiros
fake = Faker(['pt_BR'])

def gerar_cpf():
    """Gera um CPF válido usando Faker"""
    return fake.cpf().replace('.', '').replace('-', '')

def gerar_beneficio():
    """Gera um número de benefício único"""
    return str(random.randint(1000000000, 9999999999))

def gerar_numero_conta():
    """Gera um número de conta bancária"""
    return str(random.randint(1000000000, 9999999999))

def gerar_agencia():
    """Gera um número de agência"""
    return str(random.randint(1000, 9999))

def criar_cliente():
    """Cria um cliente com dados pessoais e conta bancária"""
    # Gerar dados do cliente
    nome = fake.name()
    cpf = gerar_cpf()
    beneficio = gerar_beneficio()
    estado_civil = random.choice(['S', 'C', 'D', 'V'])
    sexo = random.choice(['F', 'M'])
    nome_mae = fake.name_female()
    nome_pai = fake.name_male() if random.choice([True, False]) else "Nada Consta"
    email = fake.email()
    
    # Criar cliente
    cliente = Cliente.objects.create(
        nome=nome,
        cpf=cpf,
        beneficio=beneficio,
        estado_civil=estado_civil,
        sexo=sexo,
        nome_mae=nome_mae,
        nome_pai=nome_pai,
        email=email
    )
    
    # Criar dados pessoais (endereço)
    dados_pessoais = DadosPessoais.objects.create(
        cliente=cliente,
        cep=fake.postcode().replace('-', ''),
        rua=fake.street_name(),
        uf=fake.state_abbr(),
        numero=str(random.randint(1, 9999)),
        bairro=fake.neighborhood()
    )
    
    # Criar conta bancária
    conta = ContaBancaria.objects.create(
        cliente=cliente,
        numero_conta=gerar_numero_conta(),
        dv_conta=str(random.randint(0, 9)),
        agencia=gerar_agencia(),
        dv_agencia=str(random.randint(0, 9))
    )
    
    return cliente

def criar_emprestimos(cliente):
    """Cria 1-3 empréstimos para um cliente"""
    num_emprestimos = random.randint(1, 3)
    emprestimos = []
    
    for _ in range(num_emprestimos):
        # Gerar valores aleatórios para o empréstimo
        valor_solicitado = Decimal(str(random.randint(1000, 50000)))
        taxa_juros = Decimal(str(random.uniform(2.0, 8.0)))
        num_parcelas = random.randint(12, 60)
        
        # Criar empréstimo
        emprestimo = Emprestimo.objects.create(
            cliente=cliente,
            valor_solicitado=valor_solicitado,
            taxa_juros=taxa_juros,
            num_parcelas=num_parcelas
        )
        
        # Calcular valores totais
        emprestimo.calcular_valor_total()
        emprestimo.calcular_valor_parcela()
        
        # Aprovar automaticamente se taxa > 4%
        if taxa_juros > 4.0:
            emprestimo.aprovado = True
        
        emprestimo.save()
        emprestimos.append(emprestimo)
    
    return emprestimos

def exportar_para_csv():
    """Exporta dados de clientes e empréstimos para CSV"""
    # Exportar clientes
    clientes_data = []
    for cliente in Cliente.objects.all():
        dados_pessoais = cliente.dados_pessoais.first()
        conta = cliente.conta_bancaria
        
        clientes_data.append({
            'cpf': cliente.cpf,
            'nome': cliente.nome,
            'beneficio': cliente.beneficio,
            'estado_civil': cliente.get_estado_civil_display(),
            'sexo': cliente.get_sexo_display(),
            'nome_mae': cliente.nome_mae,
            'nome_pai': cliente.nome_pai,
            'email': cliente.email,
            'cep': dados_pessoais.cep if dados_pessoais else '',
            'rua': dados_pessoais.rua if dados_pessoais else '',
            'uf': dados_pessoais.uf if dados_pessoais else '',
            'numero': dados_pessoais.numero if dados_pessoais else '',
            'bairro': dados_pessoais.bairro if dados_pessoais else '',
            'numero_conta': conta.numero_conta if conta else '',
            'agencia': conta.agencia if conta else '',
        })
    
    # Exportar empréstimos
    emprestimos_data = []
    for emprestimo in Emprestimo.objects.all():
        emprestimos_data.append({
            'id': emprestimo.id,
            'cpf_cliente': emprestimo.cliente.cpf,
            'nome_cliente': emprestimo.cliente.nome,
            'valor_solicitado': float(emprestimo.valor_solicitado),
            'taxa_juros': float(emprestimo.taxa_juros),
            'num_parcelas': emprestimo.num_parcelas,
            'valor_total': float(emprestimo.valor_total) if emprestimo.valor_total else 0,
            'valor_parcela': float(emprestimo.valor_parcela) if emprestimo.valor_parcela else 0,
            'aprovado': emprestimo.aprovado,
            'data_solicitacao': emprestimo.data_solicitacao.strftime('%Y-%m-%d %H:%M:%S'),
        })
    
    # Salvar CSVs
    df_clientes = pd.DataFrame(clientes_data)
    df_emprestimos = pd.DataFrame(emprestimos_data)
    
    df_clientes.to_csv('clientes_gerados.csv', index=False, encoding='utf-8')
    df_emprestimos.to_csv('emprestimos_gerados.csv', index=False, encoding='utf-8')
    
    print(f"✅ Exportados {len(clientes_data)} clientes para 'clientes_gerados.csv'")
    print(f"✅ Exportados {len(emprestimos_data)} empréstimos para 'emprestimos_gerados.csv'")

def main():
    """Função principal do script"""
    print("🚀 Iniciando geração de dados da Etapa 1...")
    
    # Verificar se já existem dados
    if Cliente.objects.count() > 0:
        print("⚠️  Já existem clientes no banco. Deseja continuar? (s/n): ", end="")
        resposta = input().lower()
        if resposta != 's':
            print("❌ Operação cancelada.")
            return
    
    # Gerar 50 clientes
    print("📝 Gerando 50 clientes...")
    clientes_criados = []
    for i in range(50):
        cliente = criar_cliente()
        clientes_criados.append(cliente)
        if (i + 1) % 10 == 0:
            print(f"   ✅ Criados {i + 1}/50 clientes")
    
    # Criar empréstimos para cada cliente
    print("💰 Criando empréstimos para cada cliente...")
    total_emprestimos = 0
    emprestimos_aprovados = 0
    
    for i, cliente in enumerate(clientes_criados):
        emprestimos = criar_emprestimos(cliente)
        total_emprestimos += len(emprestimos)
        emprestimos_aprovados += sum(1 for e in emprestimos if e.aprovado)
        
        if (i + 1) % 10 == 0:
            print(f"   ✅ Processados {i + 1}/50 clientes")
    
    # Exportar dados
    print("📊 Exportando dados para CSV...")
    exportar_para_csv()
    
    # Resumo final
    print("\n" + "="*50)
    print("📈 RESUMO DA ETAPA 1")
    print("="*50)
    print(f"👥 Clientes criados: {len(clientes_criados)}")
    print(f"💰 Total de empréstimos: {total_emprestimos}")
    print(f"✅ Empréstimos aprovados: {emprestimos_aprovados}")
    print(f"❌ Empréstimos reprovados: {total_emprestimos - emprestimos_aprovados}")
    print(f"📊 Taxa de aprovação: {(emprestimos_aprovados/total_emprestimos)*100:.1f}%")
    print("="*50)
    print("✅ Etapa 1 concluída com sucesso!")

if __name__ == "__main__":
    main() 