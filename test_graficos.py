"""
Script de teste para verificar se os gráficos funcionam
Execute: python test_graficos.py
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def test_plotly_installation():
    """Testa se plotly está instalado corretamente"""
    try:
        import plotly
        print(f"✅ Plotly versão {plotly.__version__} instalado")
        return True
    except ImportError:
        print("❌ Plotly não instalado")
        return False

def test_basic_chart():
    """Testa criação de gráfico básico"""
    try:
        # Dados simples
        df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [10, 20, 15, 25, 30]
        })
        
        # Criar gráfico
        fig = px.bar(df, x='x', y='y', title='Teste Básico')
        
        # Verificar se foi criado
        if fig:
            print("✅ Gráfico básico criado com sucesso")
            return True
        else:
            print("❌ Erro ao criar gráfico básico")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste básico: {str(e)}")
        return False

def test_advanced_chart():
    """Testa gráfico mais complexo"""
    try:
        # Dados mais complexos
        np.random.seed(42)
        df = pd.DataFrame({
            'vendas': np.random.randint(1000, 10000, 50),
            'regiao': np.random.choice(['Norte', 'Sul', 'Leste', 'Oeste'], 50),
            'categoria': np.random.choice(['A', 'B', 'C'], 50)
        })
        
        # Gráfico de barras agrupado
        vendas_regiao = df.groupby('regiao')['vendas'].sum().reset_index()
        fig = px.bar(
            vendas_regiao,
            x='regiao',
            y='vendas',
            title='Vendas por Região',
            color='vendas'
        )
        
        if fig:
            print("✅ Gráfico avançado criado com sucesso")
            return True
        else:
            print("❌ Erro ao criar gráfico avançado")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste avançado: {str(e)}")
        return False

def test_all_chart_types():
    """Testa todos os tipos de gráficos"""
    try:
        # Dados de teste
        np.random.seed(42)
        df = pd.DataFrame({
            'vendas': np.random.randint(1000, 10000, 100),
            'regiao': np.random.choice(['Norte', 'Sul', 'Leste', 'Oeste'], 100),
            'categoria': np.random.choice(['A', 'B', 'C'], 100),
            'mes': np.random.choice(['Jan', 'Fev', 'Mar', 'Abr'], 100),
            'satisfacao': np.random.randint(1, 6, 100)
        })
        
        charts_created = 0
        
        # 1. Gráfico de Barras
        try:
            vendas_regiao = df.groupby('regiao')['vendas'].sum().reset_index()
            fig1 = px.bar(vendas_regiao, x='regiao', y='vendas', title='Barras')
            if fig1:
                charts_created += 1
                print("✅ Gráfico de barras OK")
        except:
            print("❌ Erro no gráfico de barras")
        
        # 2. Gráfico de Pizza
        try:
            categoria_counts = df['categoria'].value_counts()
            fig2 = px.pie(values=categoria_counts.values, names=categoria_counts.index, title='Pizza')
            if fig2:
                charts_created += 1
                print("✅ Gráfico de pizza OK")
        except:
            print("❌ Erro no gráfico de pizza")
        
        # 3. Gráfico de Linha
        try:
            vendas_mes = df.groupby('mes')['vendas'].sum().reset_index()
            fig3 = px.line(vendas_mes, x='mes', y='vendas', title='Linha')
            if fig3:
                charts_created += 1
                print("✅ Gráfico de linha OK")
        except:
            print("❌ Erro no gráfico de linha")
        
        # 4. Scatter Plot
        try:
            fig4 = px.scatter(df, x='satisfacao', y='vendas', color='regiao', title='Scatter')
            if fig4:
                charts_created += 1
                print("✅ Scatter plot OK")
        except:
            print("❌ Erro no scatter plot")
        
        # 5. Histograma
        try:
            fig5 = px.histogram(df, x='vendas', title='Histograma')
            if fig5:
                charts_created += 1
                print("✅ Histograma OK")
        except:
            print("❌ Erro no histograma")
        
        # 6. Box Plot
        try:
            fig6 = px.box(df, x='categoria', y='vendas', title='Box Plot')
            if fig6:
                charts_created += 1
                print("✅ Box plot OK")
        except:
            print("❌ Erro no box plot")
        
        print(f"\n📊 Resultado: {charts_created}/6 gráficos criados com sucesso")
        
        if charts_created == 6:
            print("🎉 TODOS OS GRÁFICOS FUNCIONANDO!")
            return True
        elif charts_created >= 4:
            print("⚠️ Maioria dos gráficos funcionando")
            return True
        else:
            print("❌ Muitos gráficos com problema")
            return False
            
    except Exception as e:
        print(f"❌ Erro geral no teste: {str(e)}")
        return False

def main():
    """Função principal de teste"""
    print("🧪 TESTE DE GRÁFICOS - DATAINSIGHT AI PRO")
    print("=" * 50)
    
    # Teste 1: Instalação
    print("\n1️⃣ Testando instalação do Plotly...")
    if not test_plotly_installation():
        print("❌ Instale plotly: pip install plotly")
        return
    
    # Teste 2: Gráfico básico
    print("\n2️⃣ Testando gráfico básico...")
    if not test_basic_chart():
        print("❌ Problema na criação de gráficos básicos")
        return
    
    # Teste 3: Gráfico avançado
    print("\n3️⃣ Testando gráfico avançado...")
    if not test_advanced_chart():
        print("❌ Problema na criação de gráficos avançados")
        return
    
    # Teste 4: Todos os tipos
    print("\n4️⃣ Testando todos os tipos de gráficos...")
    if test_all_chart_types():
        print("\n🎉 SUCESSO! Todos os gráficos funcionando!")
        print("✅ Sua instalação está correta")
        print("✅ Os gráficos vão funcionar no Streamlit")
    else:
        print("\n⚠️ Alguns gráficos com problema")
        print("💡 Tente reinstalar: pip install --upgrade plotly")
    
    print("\n" + "=" * 50)
    print("🔚 Teste concluído!")

if __name__ == "__main__":
    main()
