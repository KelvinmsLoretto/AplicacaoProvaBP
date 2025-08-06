#!/usr/bin/env python
"""
Script para comparar desempenho entre Selenium e Requests
Executa ambos os métodos de web scraping e compara tempos de execução.
"""

import time
import subprocess
import sys
import os

def executar_script(script_path):
    """Executa um script Python e retorna o tempo de execução"""
    try:
        start_time = time.time()
        
        # Executar script
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, timeout=60)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Verificar se executou com sucesso
        if result.returncode == 0:
            print(f"✅ {script_path} executado com sucesso")
            print(f"⏱️  Tempo: {execution_time:.2f} segundos")
            return execution_time
        else:
            print(f"❌ {script_path} falhou")
            print(f"Erro: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {script_path} excedeu o tempo limite (60s)")
        return None
    except Exception as e:
        print(f"❌ Erro ao executar {script_path}: {e}")
        return None

def salvar_comparacao(tempo_selenium, tempo_requests):
    """Salva a comparação de desempenho em arquivo de texto"""
    try:
        with open('performance_comparison.txt', 'w', encoding='utf-8') as f:
            f.write("=" * 50 + "\n")
            f.write("COMPARAÇÃO DE DESEMPENHO - WEB SCRAPING\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("📊 RESULTADOS:\n")
            f.write("-" * 30 + "\n")
            
            if tempo_selenium is not None:
                f.write(f"Selenium: {tempo_selenium:.2f} segundos\n")
            else:
                f.write("Selenium: Falhou ou não executou\n")
            
            if tempo_requests is not None:
                f.write(f"Requests: {tempo_requests:.2f} segundos\n")
            else:
                f.write("Requests: Falhou ou não executou\n")
            
            f.write("\n" + "=" * 50 + "\n")
            f.write("ANÁLISE:\n")
            f.write("=" * 50 + "\n\n")
            
            if tempo_selenium and tempo_requests:
                if tempo_selenium < tempo_requests:
                    f.write("🏆 Selenium foi mais rápido!\n")
                    f.write(f"Diferença: {tempo_requests - tempo_selenium:.2f} segundos\n")
                elif tempo_requests < tempo_selenium:
                    f.write("🏆 Requests foi mais rápido!\n")
                    f.write(f"Diferença: {tempo_selenium - tempo_requests:.2f} segundos\n")
                else:
                    f.write("⚖️  Ambos tiveram desempenho similar\n")
                
                f.write(f"Razão Selenium/Requests: {tempo_selenium/tempo_requests:.2f}\n")
                
            elif tempo_selenium:
                f.write("✅ Apenas Selenium funcionou\n")
                f.write("💡 Requests pode ter falhado devido ao JavaScript necessário\n")
                
            elif tempo_requests:
                f.write("✅ Apenas Requests funcionou\n")
                f.write("💡 Selenium pode ter falhado devido à configuração do driver\n")
                
            else:
                f.write("❌ Ambos os métodos falharam\n")
                f.write("💡 Verifique a configuração do ambiente\n")
            
            f.write("\n" + "=" * 50 + "\n")
            f.write("OBSERVAÇÕES:\n")
            f.write("=" * 50 + "\n\n")
            f.write("• Selenium: Melhor para sites com JavaScript dinâmico\n")
            f.write("• Requests: Mais rápido, mas limitado a conteúdo estático\n")
            f.write("• O site de demonstração pode requerer JavaScript para login\n")
            f.write("• Selenium simula um navegador real\n")
            f.write("• Requests faz requisições HTTP diretas\n")
        
        print("✅ Comparação salva em 'performance_comparison.txt'")
        
    except Exception as e:
        print(f"❌ Erro ao salvar comparação: {e}")

def main():
    """Função principal do script"""
    print("🚀 Iniciando comparação de desempenho...")
    
    # Caminhos dos scripts
    selenium_script = "scripts/webscraping/scrape_selenium.py"
    requests_script = "scripts/webscraping/scrape_requests.py"
    
    # Verificar se os scripts existem
    if not os.path.exists(selenium_script):
        print(f"❌ Script não encontrado: {selenium_script}")
        return
    
    if not os.path.exists(requests_script):
        print(f"❌ Script não encontrado: {requests_script}")
        return
    
    print("\n" + "="*50)
    print("EXECUTANDO SELENIUM")
    print("="*50)
    tempo_selenium = executar_script(selenium_script)
    
    print("\n" + "="*50)
    print("EXECUTANDO REQUESTS")
    print("="*50)
    tempo_requests = executar_script(requests_script)
    
    print("\n" + "="*50)
    print("COMPARANDO RESULTADOS")
    print("="*50)
    salvar_comparacao(tempo_selenium, tempo_requests)
    
    print("\n✅ Comparação de desempenho concluída!")

if __name__ == "__main__":
    main() 