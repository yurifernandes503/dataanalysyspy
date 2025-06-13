"""
Ferramenta de Diagnóstico para Problemas de Gráficos
Execute: python diagnostico_graficos.py
"""

import sys
import os
import platform
import subprocess
import importlib.util
import traceback

def print_header(text):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 60)
    print(f" {text} ".center(60, "="))
    print("=" * 60)

def print_section(text):
    """Imprime seção formatada"""
    print("\n" + "-" * 60)
    print(f" {text} ".center(60, "-"))
    print("-" * 60)

def check_python_version():
    """Verifica versão do Python"""
    print_section("Verificando versão do Python")
    
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ PROBLEMA: Python 3.7+ recomendado para Streamlit e bibliotecas gráficas")
    else:
        print("✅ OK: Versão do Python compatível")

def check_os():
    """Verifica sistema operacional"""
    print_section("Verificando Sistema Operacional")
    
    os_name = platform.system()
    os_version = platform.version()
    
    print(f"Sistema: {os_name}")
    print(f"Versão: {os_version}")
    
    if os_name == "Windows":
        print("ℹ️ Windows pode precisar de configurações adicionais para algumas bibliotecas gráficas")
    
    # Verificar se é ambiente virtual
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Ambiente virtual detectado")
    else:
        print("⚠️ Não está usando ambiente virtual (recomendado para evitar conflitos)")

def check_library(library_name, import_name=None):
    """Verifica se uma biblioteca está instalada e sua versão"""
    if import_name is None:
        import_name = library_name
    
    try:
        spec = importlib.util.find_spec(import_name)
        if spec is None:
            print(f"❌ {library_name}: Não instalado")
            return False, None
        
        # Tentar importar para obter versão
        module = importlib.import_module(import_name)
        version = getattr(module, "__version__", "Desconhecida")
        print(f"✅ {library_name}: Instalado (versão {version})")
        return True, version
    except Exception as e:
        print(f"❌ {library_name}: Erro ao verificar - {str(e)}")
        return False, None

def check_graphics_libraries():
    """Verifica bibliotecas gráficas"""
    print_section("Verificando Bibliotecas Gráficas")
    
    libraries = {
        "Streamlit": "streamlit",
        "Pandas": "pandas",
        "NumPy": "numpy",
        "Matplotlib": "matplotlib",
        "Plotly": "plotly",
        "Altair": "altair",
        "Seaborn": "seaborn"
    }
    
    results = {}
    for name, import_name in libraries.items():
        installed, version = check_library(name, import_name)
        results[name] = (installed, version)
    
    return results

def test_matplotlib():
    """Testa se o Matplotlib funciona"""
    print_section("Testando Matplotlib")
    
    try:
        import matplotlib
        matplotlib.use('Agg')  # Backend não-interativo
        import matplotlib.pyplot as plt
        import numpy as np
        
        # Criar figura simples
        plt.figure(figsize=(2, 2))
        plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
        plt.title("Test")
        
        # Salvar em memória
        import io
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        
        # Verificar se o buffer tem conteúdo
        if len(buf.getvalue()) > 0:
            print("✅ Matplotlib: Gráfico gerado com sucesso")
        else:
            print("❌ Matplotlib: Falha ao gerar gráfico")
        
        plt.close()
        
    except Exception as e:
        print(f"❌ Matplotlib: Erro - {str(e)}")
        print(traceback.format_exc())

def test_plotly():
    """Testa se o Plotly funciona"""
    print_section("Testando Plotly")
    
    try:
        import plotly.graph_objects as go
        
        # Criar figura simples
        fig = go.Figure(data=go.Bar(y=[2, 3, 1]))
        
        # Verificar se a figura foi criada
        if fig:
            print("✅ Plotly: Figura criada com sucesso")
        else:
            print("❌ Plotly: Falha ao criar figura")
            
    except Exception as e:
        print(f"❌ Plotly: Erro - {str(e)}")
        print(traceback.format_exc())

def check_streamlit():
    """Verifica configuração do Streamlit"""
    print_section("Verificando Streamlit")
    
    try:
        import streamlit as st
        print(f"✅ Streamlit versão {st.__version__}")
        
        # Verificar arquivo de configuração
        config_path = os.path.expanduser("~/.streamlit/config.toml")
        if os.path.exists(config_path):
            print(f"✅ Arquivo de configuração encontrado: {config_path}")
            
            # Ler configurações relevantes
            try:
                with open(config_path, 'r') as f:
                    content = f.read()
                    if "browser.gatherUsageStats = false" in content:
                        print("ℹ️ Coleta de estatísticas desativada")
                    if "runner.installTracer = false" in content:
                        print("ℹ️ Tracer desativado")
            except:
                pass
        else:
            print("ℹ️ Arquivo de configuração não encontrado (usando padrões)")
        
    except Exception as e:
        print(f"❌ Streamlit: Erro - {str(e)}")

def suggest_fixes(library_results):
    """Sugere correções com base nos resultados"""
    print_section("Sugestões de Correção")
    
    # Verificar quais bibliotecas estão faltando
    missing = [name for name, (installed, _) in library_results.items() if not installed]
    
    if missing:
        print(f"❌ Bibliotecas faltando: {', '.join(missing)}")
        
        # Comando para instalar
        install_cmd = "pip install " + " ".join(missing).lower()
        print(f"\nComando para instalar:")
        print(f"  {install_cmd}")
    else:
        print("✅ Todas as bibliotecas principais estão instaladas")
    
    # Verificar Matplotlib
    if library_results.get("Matplotlib", (False, None))[0]:
        print("\nPara problemas com Matplotlib:")
        print("  1. Tente usar o backend 'Agg':")
        print("     import matplotlib")
        print("     matplotlib.use('Agg')")
        print("  2. Reinstale com:")
        print("     pip uninstall matplotlib -y && pip install matplotlib")
    
    # Verificar Plotly
    if library_results.get("Plotly", (False, None))[0]:
        print("\nPara problemas com Plotly:")
        print("  1. Reinstale com versão específica:")
        print("     pip uninstall plotly -y && pip install plotly==5.17.0")
        print("  2. Verifique se plotly.js está sendo carregado no navegador")
    
    # Sugestões gerais
    print("\nSugestões gerais:")
    print("  1. Use ambiente virtual para evitar conflitos:")
    print("     python -m venv venv")
    print("     source venv/bin/activate  # Linux/Mac")
    print("     venv\\Scripts\\activate  # Windows")
    print("  2. Atualize pip:")
    print("     pip install --upgrade pip")
    print("  3. Limpe o cache do Streamlit:")
    print("     rm -rf ~/.streamlit  # Linux/Mac")
    print("     rmdir /s /q %userprofile%\\.streamlit  # Windows")
    print("  4. Use a versão ultra simplificada:")
    print("     streamlit run graficos_ascii.py")
    print("     streamlit run graficos_html_puro.py")

def main():
    """Função principal"""
    print_header("DIAGNÓSTICO DE PROBLEMAS COM GRÁFICOS")
    print("Ferramenta para identificar e resolver problemas com gráficos")
    
    # Verificar ambiente
    check_python_version()
    check_os()
    
    # Verificar bibliotecas
    library_results = check_graphics_libraries()
    
    # Testar bibliotecas gráficas
    if library_results.get("Matplotlib", (False, None))[0]:
        test_matplotlib()
    
    if library_results.get("Plotly", (False, None))[0]:
        test_plotly()
    
    # Verificar Streamlit
    check_streamlit()
    
    # Sugerir correções
    suggest_fixes(library_results)
    
    print_header("DIAGNÓSTICO CONCLUÍDO")
    print("Execute uma das versões simplificadas para garantir que os gráficos funcionem:")
    print("  1. streamlit run graficos_garantidos.py  # Múltiplos fallbacks")
    print("  2. streamlit run graficos_ascii.py       # Funciona em qualquer lugar")
    print("  3. streamlit run graficos_html_puro.py   # Visualizações HTML puras")

if __name__ == "__main__":
    main()
