"""
Script para corrigir problemas com gráficos
Execute: python fix_graficos.py
"""

import subprocess
import sys
import os

def run_command(command):
    """Executa comando e retorna resultado"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def fix_plotly():
    """Corrige problemas com plotly"""
    print("🔧 Corrigindo instalação do Plotly...")
    
    # Desinstalar plotly
    print("1. Desinstalando plotly atual...")
    success, stdout, stderr = run_command("pip uninstall plotly -y")
    if success:
        print("✅ Plotly desinstalado")
    else:
        print(f"⚠️ Aviso: {stderr}")
    
    # Limpar cache
    print("2. Limpando cache...")
    run_command("pip cache purge")
    
    # Reinstalar plotly
    print("3. Reinstalando plotly...")
    success, stdout, stderr = run_command("pip install plotly==5.17.0 --no-cache-dir")
    if success:
        print("✅ Plotly reinstalado com sucesso")
    else:
        print(f"❌ Erro: {stderr}")
        return False
    
    return True

def fix_dependencies():
    """Corrige todas as dependências"""
    print("🔧 Corrigindo todas as dependências...")
    
    dependencies = [
        "streamlit==1.29.0",
        "pandas==2.1.3", 
        "numpy==1.24.3",
        "plotly==5.17.0",
        "google-generativeai==0.3.2",
        "openpyxl==3.1.2"
    ]
    
    for dep in dependencies:
        print(f"Instalando {dep}...")
        success, stdout, stderr = run_command(f"pip install {dep} --force-reinstall --no-cache-dir")
        if success:
            print(f"✅ {dep} OK")
        else:
            print(f"❌ Erro em {dep}: {stderr}")

def test_imports():
    """Testa se todas as importações funcionam"""
    print("🧪 Testando importações...")
    
    imports_to_test = [
        ("streamlit", "st"),
        ("pandas", "pd"),
        ("numpy", "np"),
        ("plotly.express", "px"),
        ("plotly.graph_objects", "go"),
        ("google.generativeai", "genai")
    ]
    
    all_ok = True
    
    for module, alias in imports_to_test:
        try:
            exec(f"import {module} as {alias}")
            print(f"✅ {module} OK")
        except ImportError as e:
            print(f"❌ {module} ERRO: {e}")
            all_ok = False
    
    return all_ok

def create_test_chart():
    """Cria gráfico de teste"""
    print("📊 Testando criação de gráfico...")
    
    try:
        import pandas as pd
        import plotly.express as px
        
        # Dados simples
        df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [10, 20, 15, 25, 30]
        })
        
        # Criar gráfico
        fig = px.bar(df, x='x', y='y', title='Teste')
        
        if fig:
            print("✅ Gráfico criado com sucesso!")
            return True
        else:
            print("❌ Erro ao criar gráfico")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    """Função principal"""
    print("🛠️ CORRETOR DE GRÁFICOS - DATAINSIGHT AI PRO")
    print("=" * 50)
    
    # Verificar Python
    print(f"🐍 Python: {sys.version}")
    
    # Opções de correção
    print("\nEscolha uma opção:")
    print("1. Corrigir apenas Plotly")
    print("2. Corrigir todas as dependências")
    print("3. Apenas testar importações")
    print("4. Correção completa (recomendado)")
    
    choice = input("\nDigite sua escolha (1-4): ").strip()
    
    if choice == "1":
        fix_plotly()
    elif choice == "2":
        fix_dependencies()
    elif choice == "3":
        test_imports()
    elif choice == "4":
        print("\n🚀 Iniciando correção completa...")
        fix_dependencies()
        print("\n" + "-" * 30)
        test_imports()
        print("\n" + "-" * 30)
        create_test_chart()
    else:
        print("❌ Opção inválida")
        return
    
    print("\n" + "=" * 50)
    print("✅ Correção concluída!")
    print("💡 Agora execute: streamlit run app.py")

if __name__ == "__main__":
    main()
