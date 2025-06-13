import streamlit as st
import pandas as pd
import numpy as np
import time
import os
import sys
import io
import base64
from datetime import datetime

# Configuração básica
st.set_page_config(
    page_title="Gráficos Garantidos",
    page_icon="📊",
    layout="wide"
)

# CSS mínimo para não interferir com o funcionamento
st.markdown("""
<style>
    .header {
        text-align: center;
        padding: 1rem;
        background-color: #f0f2f6;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .success {
        color: green;
        font-weight: bold;
    }
    .error {
        color: red;
        font-weight: bold;
    }
    .warning {
        color: orange;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header simples
st.markdown("""
<div class="header">
    <h1>📊 Sistema de Gráficos Garantidos</h1>
    <p>Versão ultra simplificada para garantir funcionamento</p>
</div>
""", unsafe_allow_html=True)

# Função para verificar e instalar bibliotecas
def check_and_install_libraries():
    libraries = {
        'matplotlib': False,
        'plotly': False,
        'altair': False,
        'streamlit': True  # Já está instalado se estamos rodando
    }
    
    # Verificar matplotlib
    try:
        import matplotlib.pyplot as plt
        libraries['matplotlib'] = True
    except:
        st.warning("⚠️ Matplotlib não encontrado")
    
    # Verificar plotly
    try:
        import plotly.express as px
        libraries['plotly'] = True
    except:
        st.warning("⚠️ Plotly não encontrado")
    
    # Verificar altair (usado pelo streamlit)
    try:
        import altair as alt
        libraries['altair'] = True
    except:
        st.warning("⚠️ Altair não encontrado")
    
    return libraries

# Função para gerar dados simples
def generate_simple_data():
    # Dados super simples para minimizar problemas
    data = {
        'categoria': ['A', 'B', 'C', 'D', 'E'],
        'valores': [10, 25, 15, 30, 20]
    }
    return pd.DataFrame(data)

# Função para gerar dados mais complexos
def generate_sales_data():
    np.random.seed(42)
    
    # Dados de vendas simples
    regioes = ['Norte', 'Sul', 'Leste', 'Oeste', 'Centro']
    produtos = ['Produto A', 'Produto B', 'Produto C']
    
    data = []
    for _ in range(100):
        regiao = np.random.choice(regioes)
        produto = np.random.choice(produtos)
        vendas = np.random.randint(1000, 10000)
        lucro = int(vendas * np.random.uniform(0.1, 0.4))
        
        data.append({
            'regiao': regiao,
            'produto': produto,
            'vendas': vendas,
            'lucro': lucro
        })
    
    return pd.DataFrame(data)

# Função para criar gráfico com matplotlib (método 1)
def create_matplotlib_chart(df, x_col, y_col, title):
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')  # Não interativo, evita problemas
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df[x_col], df[y_col], color='skyblue')
        ax.set_title(title)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        
        # Adicionar valores nas barras
        for i, v in enumerate(df[y_col]):
            ax.text(i, v + 0.5, str(v), ha='center')
        
        # Usar buffer para evitar problemas de arquivo
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        
        # Converter para base64 para exibir como imagem
        img_str = base64.b64encode(buf.read()).decode()
        
        # Exibir como HTML para garantir que funcione
        st.markdown(f'<img src="data:image/png;base64,{img_str}" alt="{title}" width="100%">', unsafe_allow_html=True)
        
        plt.close(fig)  # Importante para liberar memória
        return True
    except Exception as e:
        st.error(f"Erro no matplotlib: {str(e)}")
        return False

# Função para criar gráfico com plotly (método 2)
def create_plotly_chart(df, x_col, y_col, title):
    try:
        import plotly.express as px
        
        fig = px.bar(df, x=x_col, y=y_col, title=title)
        st.plotly_chart(fig, use_container_width=True)
        return True
    except Exception as e:
        st.error(f"Erro no plotly: {str(e)}")
        return False

# Função para criar gráfico com altair (método 3)
def create_altair_chart(df, x_col, y_col, title):
    try:
        import altair as alt
        
        chart = alt.Chart(df).mark_bar().encode(
            x=x_col,
            y=y_col,
            tooltip=[x_col, y_col]
        ).properties(
            title=title
        )
        
        st.altair_chart(chart, use_container_width=True)
        return True
    except Exception as e:
        st.error(f"Erro no altair: {str(e)}")
        return False

# Função para criar gráfico nativo do streamlit (método 4 - garantido)
def create_streamlit_native_chart(df, x_col, y_col, title):
    try:
        st.subheader(title)
        chart_data = df.set_index(x_col)[[y_col]]
        st.bar_chart(chart_data)
        return True
    except Exception as e:
        st.error(f"Erro no gráfico nativo: {str(e)}")
        return False

# Função para criar gráfico HTML puro (método 5 - último recurso)
def create_html_chart(df, x_col, y_col, title):
    try:
        # Criar um gráfico HTML simples
        html = f"""
        <h3>{title}</h3>
        <div style="display: flex; align-items: flex-end; height: 300px; background-color: #f9f9f9; padding: 10px; border-radius: 5px;">
        """
        
        max_val = df[y_col].max()
        
        for i, row in df.iterrows():
            x = row[x_col]
            y = row[y_col]
            height_percent = (y / max_val) * 100 if max_val > 0 else 0
            
            html += f"""
            <div style="display: flex; flex-direction: column; align-items: center; margin: 0 10px;">
                <div style="height: {height_percent}%; width: 40px; background-color: #4CAF50; margin-bottom: 5px;"></div>
                <div>{x}</div>
                <div>{y}</div>
            </div>
            """
        
        html += "</div>"
        
        st.markdown(html, unsafe_allow_html=True)
        return True
    except Exception as e:
        st.error(f"Erro no HTML: {str(e)}")
        return False

# Função para criar gráfico ASCII (método 6 - último recurso absoluto)
def create_ascii_chart(df, x_col, y_col, title):
    try:
        st.subheader(title)
        
        # Normalizar para altura máxima de 10 caracteres
        max_val = df[y_col].max()
        scale_factor = 10 / max_val if max_val > 0 else 0
        
        ascii_chart = ""
        
        # Criar barras ASCII
        for i, row in df.iterrows():
            x = row[x_col]
            y = row[y_col]
            bar_height = int(y * scale_factor)
            
            ascii_chart += f"{x}: {'█' * bar_height} {y}\n"
        
        st.code(ascii_chart)
        return True
    except Exception as e:
        st.error(f"Erro no ASCII: {str(e)}")
        return False

# Função principal para criar gráficos com múltiplos fallbacks
def create_guaranteed_chart(df, x_col, y_col, title):
    st.subheader("🔍 Tentando criar gráfico...")
    
    # Verificar se as colunas existem
    if x_col not in df.columns or y_col not in df.columns:
        st.error(f"Colunas {x_col} ou {y_col} não encontradas no DataFrame")
        return False
    
    # Verificar se há dados suficientes
    if len(df) == 0:
        st.error("DataFrame vazio")
        return False
    
    # Tentar cada método em sequência
    methods = [
        ("Plotly", create_plotly_chart),
        ("Matplotlib", create_matplotlib_chart),
        ("Altair", create_altair_chart),
        ("Streamlit Nativo", create_streamlit_native_chart),
        ("HTML", create_html_chart),
        ("ASCII", create_ascii_chart)
    ]
    
    for method_name, method_func in methods:
        st.write(f"Tentando método: {method_name}...")
        
        try:
            success = method_func(df, x_col, y_col, title)
            if success:
                st.success(f"✅ Gráfico criado com sucesso usando {method_name}!")
                return True
        except Exception as e:
            st.warning(f"⚠️ {method_name} falhou: {str(e)}")
    
    st.error("❌ Todos os métodos falharam. Impossível criar gráfico.")
    return False

# Função para criar tabela de dados (fallback final)
def show_data_table(df, title):
    st.subheader(title)
    st.dataframe(df)

# Sidebar
st.sidebar.title("📊 Controles")

# Verificar bibliotecas
st.sidebar.subheader("Diagnóstico do Sistema")
libraries = check_and_install_libraries()

for lib, status in libraries.items():
    if status:
        st.sidebar.success(f"✅ {lib} disponível")
    else:
        st.sidebar.warning(f"⚠️ {lib} não disponível")

# Opções de dados
st.sidebar.subheader("Dados")
data_option = st.sidebar.radio(
    "Escolha os dados:",
    ["Dados Simples", "Dados de Vendas"]
)

# Botão para gerar gráficos
if st.sidebar.button("📊 Gerar Gráficos Garantidos", use_container_width=True):
    
    # Gerar dados conforme seleção
    if data_option == "Dados Simples":
        df = generate_simple_data()
        x_col = 'categoria'
        y_col = 'valores'
    else:
        df = generate_sales_data()
        # Agregar por região
        df_region = df.groupby('regiao').agg({'vendas': 'sum'}).reset_index()
        x_col = 'regiao'
        y_col = 'vendas'
        df = df_region
    
    # Mostrar dados
    st.subheader("📋 Dados para Visualização")
    st.dataframe(df)
    
    # Criar gráficos garantidos
    st.markdown("---")
    st.subheader("📊 Gráficos Garantidos")
    
    # Mostrar progresso
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(101):
        progress_bar.progress(i)
        if i < 30:
            status_text.text("Preparando dados...")
        elif i < 60:
            status_text.text("Verificando bibliotecas disponíveis...")
        elif i < 90:
            status_text.text("Gerando visualizações...")
        else:
            status_text.text("Finalizando...")
        time.sleep(0.01)
    
    status_text.empty()
    progress_bar.empty()
    
    # Criar gráfico principal
    success = create_guaranteed_chart(df, x_col, y_col, "Gráfico Principal")
    
    if success:
        st.balloons()
    else:
        # Último recurso: mostrar tabela
        st.error("Não foi possível criar nenhum gráfico. Mostrando dados em formato de tabela.")
        show_data_table(df, "Dados em Tabela")

# Instruções
st.sidebar.markdown("---")
st.sidebar.subheader("📝 Instruções")
st.sidebar.info("""
1. Escolha o tipo de dados
2. Clique em "Gerar Gráficos Garantidos"
3. O sistema tentará múltiplos métodos
4. Pelo menos um método funcionará!
""")

# Informações de diagnóstico
st.sidebar.markdown("---")
st.sidebar.subheader("🔧 Diagnóstico")
st.sidebar.info(f"""
- Python: {sys.version.split()[0]}
- Pandas: {pd.__version__}
- Numpy: {np.__version__}
- Streamlit: {st.__version__}
- OS: {os.name}
""")

# Área principal - Instruções iniciais
if 'button_clicked' not in st.session_state:
    st.markdown("""
    ## 🎯 Sistema Ultra Simplificado para Gráficos Garantidos
    
    Este sistema foi projetado com um único objetivo: **garantir que os gráficos funcionem**, não importa o que aconteça.
    
    ### 🛠️ Características:
    
    - **6 métodos diferentes** de renderização de gráficos
    - Fallbacks automáticos se um método falhar
    - Diagnóstico detalhado de problemas
    - Funciona mesmo com bibliotecas limitadas
    - Último recurso: gráficos ASCII que funcionam em qualquer lugar!
    
    ### 📊 Bibliotecas suportadas:
    
    1. **Plotly** - Gráficos interativos avançados
    2. **Matplotlib** - Gráficos estáticos confiáveis
    3. **Altair** - Gráficos declarativos
    4. **Streamlit nativo** - Gráficos básicos integrados
    5. **HTML puro** - Renderização direta no navegador
    6. **ASCII** - Funciona em qualquer terminal!
    
    ### 🚀 Como começar:
    
    Clique no botão **"Gerar Gráficos Garantidos"** no menu lateral para começar.
    """)

# Footer
st.markdown("---")
st.markdown("📊 **Sistema de Gráficos Garantidos** - Versão Ultra Simplificada")
