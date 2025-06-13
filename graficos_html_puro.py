import streamlit as st
import pandas as pd
import numpy as np
import time
import random

# Configuração básica
st.set_page_config(
    page_title="Gráficos HTML Puros",
    page_icon="📊",
    layout="wide"
)

# CSS para os gráficos HTML
st.markdown("""
<style>
    .html-chart-container {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    .html-chart-title {
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    
    .html-bar-chart {
        display: flex;
        align-items: flex-end;
        height: 300px;
        padding: 10px 0;
    }
    
    .html-bar {
        flex: 1;
        margin: 0 5px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .html-bar-value {
        background-color: #4CAF50;
        width: 40px;
        transition: height 1s ease-in-out;
    }
    
    .html-bar-label {
        margin-top: 10px;
        text-align: center;
        font-size: 12px;
    }
    
    .html-bar-text {
        margin-top: 5px;
        font-weight: bold;
    }
    
    .html-pie-chart {
        width: 300px;
        height: 300px;
        border-radius: 50%;
        margin: 0 auto;
        background: conic-gradient(
            #FF6384 0% 30%,
            #36A2EB 30% 55%,
            #FFCE56 55% 70%,
            #4BC0C0 70% 85%,
            #9966FF 85% 100%
        );
        position: relative;
    }
    
    .html-pie-legend {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        margin-top: 20px;
    }
    
    .html-pie-legend-item {
        display: flex;
        align-items: center;
        margin: 5px 10px;
    }
    
    .html-pie-legend-color {
        width: 15px;
        height: 15px;
        margin-right: 5px;
    }
    
    .html-line-chart {
        height: 300px;
        position: relative;
        padding: 20px 40px;
    }
    
    .html-line-point {
        position: absolute;
        width: 10px;
        height: 10px;
        background-color: #4CAF50;
        border-radius: 50%;
        transform: translate(-50%, -50%);
    }
    
    .html-line-segment {
        position: absolute;
        height: 2px;
        background-color: #4CAF50;
        transform-origin: left center;
    }
    
    .html-line-label {
        position: absolute;
        bottom: 0;
        transform: translateX(-50%);
        text-align: center;
        font-size: 12px;
    }
    
    .html-line-value {
        position: absolute;
        left: 0;
        transform: translateY(50%);
        font-size: 12px;
    }
    
    .html-table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .html-table th, .html-table td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    
    .html-table th {
        background-color: #f2f2f2;
        font-weight: bold;
    }
    
    .html-table tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    
    .html-table tr:hover {
        background-color: #f1f1f1;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📊 Gráficos HTML Puros")
st.write("Visualizações garantidas sem dependências de bibliotecas gráficas")

# Função para gerar dados de vendas
def generate_sales_data():
    regioes = ['Norte', 'Sul', 'Leste', 'Oeste', 'Centro']
    vendas = [random.randint(5000, 10000) for _ in range(len(regioes))]
    
    data = {
        'regiao': regioes,
        'vendas': vendas
    }
    
    return pd.DataFrame(data)

# Função para gerar dados de tendência
def generate_trend_data():
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
    
    # Criar tendência com alguma aleatoriedade
    base = 5000
    tendencia = []
    for i in range(len(meses)):
        valor = base + i * 500 + random.randint(-300, 300)
        tendencia.append(valor)
    
    data = {
        'mes': meses,
        'vendas': tendencia
    }
    
    return pd.DataFrame(data)

# Função para criar gráfico de barras HTML
def create_html_bar_chart(df, x_col, y_col, title):
    # Calcular altura máxima para normalização
    max_val = df[y_col].max()
    
    html = f"""
    <div class="html-chart-container">
        <div class="html-chart-title">{title}</div>
        <div class="html-bar-chart">
    """
    
    # Criar barras
    for i, row in df.iterrows():
        x = row[x_col]
        y = row[y_col]
        height_percent = (y / max_val) * 100 if max_val > 0 else 0
        
        html += f"""
        <div class="html-bar">
            <div class="html-bar-value" style="height: {height_percent}%;"></div>
            <div class="html-bar-label">{x}</div>
            <div class="html-bar-text">{y:,}</div>
        </div>
        """
    
    html += """
        </div>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)
    return True

# Função para criar gráfico de pizza HTML
def create_html_pie_chart(df, category_col, value_col, title):
    # Calcular percentuais
    total = df[value_col].sum()
    df['percent'] = df[value_col] / total * 100
    
    # Gerar gradiente cônico
    colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']
    gradient_stops = []
    current_percent = 0
    
    for i, row in df.iterrows():
        color = colors[i % len(colors)]
        start_percent = current_percent
        current_percent += row['percent']
        gradient_stops.append(f"{color} {start_percent:.1f}% {current_percent:.1f}%")
    
    gradient = ", ".join(gradient_stops)
    
    html = f"""
    <div class="html-chart-container">
        <div class="html-chart-title">{title}</div>
        <div class="html-pie-chart" style="background: conic-gradient({gradient});"></div>
        <div class="html-pie-legend">
    """
    
    # Criar legenda
    for i, row in df.iterrows():
        color = colors[i % len(colors)]
        category = row[category_col]
        value = row[value_col]
        percent = row['percent']
        
        html += f"""
        <div class="html-pie-legend-item">
            <div class="html-pie-legend-color" style="background-color: {color};"></div>
            <div>{category}: {value:,} ({percent:.1f}%)</div>
        </div>
        """
    
    html += """
        </div>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)
    return True

# Função para criar gráfico de linha HTML
def create_html_line_chart(df, x_col, y_col, title):
    # Calcular valores mínimos e máximos para normalização
    min_val = df[y_col].min()
    max_val = df[y_col].max()
    value_range = max_val - min_val
    
    # Largura de cada ponto
    width_percent = 100 / (len(df) - 1) if len(df) > 1 else 100
    
    html = f"""
    <div class="html-chart-container">
        <div class="html-chart-title">{title}</div>
        <div class="html-line-chart">
    """
    
    # Adicionar linhas de grade horizontais
    for i in range(5):
        percent = 20 * i
        grid_value = max_val - (value_range * percent / 100)
        html += f"""
        <div style="position: absolute; left: 40px; right: 20px; top: {percent}%; height: 1px; background-color: #ddd;"></div>
        <div class="html-line-value" style="top: {percent}%;">{grid_value:,.0f}</div>
        """
    
    # Adicionar pontos e linhas
    points = []
    for i, row in df.iterrows():
        x = i * width_percent
        y_normalized = ((row[y_col] - min_val) / value_range) * 100 if value_range > 0 else 50
        y = 100 - y_normalized  # Inverter para que valores maiores fiquem no topo
        
        points.append((x, y, row[x_col], row[y_col]))
        
        # Adicionar rótulo do eixo X
        html += f"""
        <div class="html-line-label" style="left: {x}%;">{row[x_col]}</div>
        """
    
    # Adicionar linhas entre pontos
    for i in range(len(points) - 1):
        x1, y1, _, _ = points[i]
        x2, y2, _, _ = points[i + 1]
        
        # Calcular comprimento e ângulo da linha
        length = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
        
        html += f"""
        <div class="html-line-segment" 
             style="left: {x1}%; top: {y1}%; 
                    width: {length}%; 
                    transform: rotate({angle}deg);"></div>
        """
    
    # Adicionar pontos
    for x, y, label, value in points:
        html += f"""
        <div class="html-line-point" style="left: {x}%; top: {y}%;" 
             title="{label}: {value:,}"></div>
        """
    
    html += """
        </div>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)
    return True

# Função para criar tabela HTML
def create_html_table(df, title):
    html = f"""
    <div class="html-chart-container">
        <div class="html-chart-title">{title}</div>
        <table class="html-table">
            <thead>
                <tr>
    """
    
    # Cabeçalhos
    for col in df.columns:
        html += f"<th>{col}</th>"
    
    html += """
                </tr>
            </thead>
            <tbody>
    """
    
    # Linhas de dados
    for i, row in df.iterrows():
        html += "<tr>"
        for col in df.columns:
            value = row[col]
            # Formatar números
            if isinstance(value, (int, float)):
                html += f"<td>{value:,}</td>"
            else:
                html += f"<td>{value}</td>"
        html += "</tr>"
    
    html += """
            </tbody>
        </table>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)
    return True

# Sidebar
st.sidebar.title("📊 Controles")

# Botão para gerar gráficos
if st.sidebar.button("📊 Gerar Gráficos HTML", use_container_width=True):
    
    # Gerar dados
    df_vendas = generate_sales_data()
    df_tendencia = generate_trend_data()
    
    # Mostrar dados
    st.subheader("📋 Dados para Visualização")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("Dados de Vendas por Região")
        st.dataframe(df_vendas)
    
    with col2:
        st.write("Dados de Tendência Mensal")
        st.dataframe(df_tendencia)
    
    # Criar gráficos HTML
    st.markdown("---")
    st.subheader("📊 Gráficos HTML Puros")
    
    # Mostrar progresso
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(101):
        progress_bar.progress(i)
        status_text.text(f"Gerando visualizações... {i}%")
        time.sleep(0.01)
    
    status_text.empty()
    progress_bar.empty()
    
    # Criar gráficos HTML
    col1, col2 = st.columns(2)
    
    with col1:
        create_html_bar_chart(df_vendas, 'regiao', 'vendas', "Vendas por Região")
        create_html_line_chart(df_tendencia, 'mes', 'vendas', "Tendência de Vendas Mensais")
    
    with col2:
        create_html_pie_chart(df_vendas, 'regiao', 'vendas', "Distribuição de Vendas por Região")
        create_html_table(df_vendas, "Tabela de Vendas por Região")
    
    st.success("✅ Gráficos HTML gerados com sucesso!")
    st.balloons()

# Instruções
st.sidebar.markdown("---")
st.sidebar.subheader("📝 Instruções")
st.sidebar.info("""
1. Clique em "Gerar Gráficos HTML"
2. O sistema criará visualizações em HTML puro
3. Funciona sem bibliotecas gráficas
4. Visualizações interativas e responsivas
""")

# Área principal - Instruções iniciais
if 'button_clicked' not in st.session_state:
    st.markdown("""
    ## 🎯 Sistema de Gráficos HTML Puros
    
    Este sistema foi projetado para criar visualizações de dados usando **apenas HTML e CSS**, sem depender de bibliotecas gráficas externas.
    
    ### 🛠️ Características:
    
    - **Zero dependências** de bibliotecas gráficas
    - Funciona em qualquer navegador
    - Visualizações responsivas
    - Animações suaves
    - Interatividade básica
    
    ### 📊 Tipos de gráficos:
    
    1. **Gráficos de Barras HTML** - Barras verticais com animação
    2. **Gráficos de Pizza HTML** - Usando gradientes cônicos CSS
    3. **Gráficos de Linha HTML** - Pontos conectados com linhas
    4. **Tabelas HTML** - Dados formatados em tabela estilizada
    
    ### 🚀 Como começar:
    
    Clique no botão **"Gerar Gráficos HTML"** no menu lateral para começar.
    """)

# Footer
st.markdown("---")
st.markdown("📊 **Sistema de Gráficos HTML Puros** - Visualizações sem dependências!")
