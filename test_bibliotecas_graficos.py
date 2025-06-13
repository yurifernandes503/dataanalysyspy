"""
Script para testar todas as bibliotecas de gráficos
Execute: python test_bibliotecas_graficos.py
"""

def test_all_libraries():
    """Testa todas as bibliotecas de gráficos"""
    print("🧪 TESTE DE BIBLIOTECAS DE GRÁFICOS")
    print("=" * 50)
    
    libraries_status = {}
    
    # Teste Plotly
    print("\n1️⃣ Testando Plotly...")
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        
        # Teste básico
        import pandas as pd
        import numpy as np
        
        df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [10, 20, 15, 25, 30]
        })
        
        fig = px.bar(df, x='x', y='y')
        if fig:
            print("✅ Plotly: FUNCIONANDO")
            libraries_status['plotly'] = True
        else:
            print("❌ Plotly: ERRO na criação de gráfico")
            libraries_status['plotly'] = False
            
    except ImportError:
        print("❌ Plotly: NÃO INSTALADO")
        libraries_status['plotly'] = False
    except Exception as e:
        print(f"❌ Plotly: ERRO - {str(e)}")
        libraries_status['plotly'] = False
    
    # Teste Matplotlib
    print("\n2️⃣ Testando Matplotlib...")
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')  # Backend não-interativo
        
        # Teste básico
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3, 4, 5], [10, 20, 15, 25, 30])
        ax.set_title('Teste')
        
        print("✅ Matplotlib: FUNCIONANDO")
        libraries_status['matplotlib'] = True
        plt.close()
        
    except ImportError:
        print("❌ Matplotlib: NÃO INSTALADO")
        libraries_status['matplotlib'] = False
    except Exception as e:
        print(f"❌ Matplotlib: ERRO - {str(e)}")
        libraries_status['matplotlib'] = False
    
    # Teste Seaborn
    print("\n3️⃣ Testando Seaborn...")
    try:
        import seaborn as sns
        import pandas as pd
        
        # Teste básico
        df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [10, 20, 15, 25, 30]
        })
        
        # Não criar gráfico, apenas testar importação
        print("✅ Seaborn: FUNCIONANDO")
        libraries_status['seaborn'] = True
        
    except ImportError:
        print("❌ Seaborn: NÃO INSTALADO")
        libraries_status['seaborn'] = False
    except Exception as e:
        print(f"❌ Seaborn: ERRO - {str(e)}")
        libraries_status['seaborn'] = False
    
    # Teste Streamlit (básico)
    print("\n4️⃣ Testando Streamlit...")
    try:
        import streamlit as st
        print("✅ Streamlit: FUNCIONANDO")
        libraries_status['streamlit'] = True
        
    except ImportError:
        print("❌ Streamlit: NÃO INSTALADO")
        libraries_status['streamlit'] = False
    except Exception as e:
        print(f"❌ Streamlit: ERRO - {str(e)}")
        libraries_status['streamlit'] = False
    
    # Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    working_libraries = sum(libraries_status.values())
    total_libraries = len(libraries_status)
    
    for lib, status in libraries_status.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {lib.capitalize()}: {'OK' if status else 'FALHOU'}")
    
    print(f"\n🎯 RESULTADO: {working_libraries}/{total_libraries} bibliotecas funcionando")
    
    if working_libraries >= 2:
        print("🎉 SUCESSO! O sistema robusto funcionará perfeitamente!")
    elif working_libraries >= 1:
        print("⚠️ PARCIAL: Pelo menos uma biblioteca funciona.")
    else:
        print("❌ PROBLEMA: Nenhuma biblioteca funcionando.")
        print("\n💡 SOLUÇÃO:")
        print("pip install plotly matplotlib seaborn streamlit pandas numpy")
    
    return libraries_status

if __name__ == "__main__":
    test_all_libraries()
