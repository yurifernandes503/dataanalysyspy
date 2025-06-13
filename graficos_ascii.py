import streamlit as st
import pandas as pd
import numpy as np
import time

# Configuração básica
st.set_page_config(
    page_title="Gráficos ASCII Garantidos",
    page_icon="📊",
    layout="wide"
)

# Header simples
st.title("📊 Gráficos ASCII Garantidos")
st.write("Versão ultra simplificada que funciona em QUALQUER ambiente")

# Função para gerar dados simples
def generate_simple_data():
    # Dados super simples para minimizar problemas
    data = {
        'categoria': ['Norte', 'Sul', 'Leste', 'Oeste', 'Centro'],
        'vendas': [5420, 8130, 6743, 9552, 7201]
    }
    return pd.DataFrame(data)

# Função para criar gráfico ASCII (funciona em QUALQUER lugar)
def create_ascii_chart(df, x_col, y_col, title):
    st.subheader(title)
    
    # Normalizar para altura máxima de 20 caracteres
    max_val = df[y_col].max()
    scale_factor = 20 / max_val if max_val > 0 else 0
    
    ascii_chart = ""
    
    # Criar barras ASCII
    for i, row in df.iterrows():
        x = row[x_col]
        y = row[y_col]
        bar_height = int(y * scale_factor)
        
        # Adicionar padding para alinhar valores
        x_padded = f"{x:<10}"
        y_padded = f"{y:>8}"
        
        ascii_chart += f"{x_padded} | {'█' * bar_height} {y_padded}\n"
    
    # Adicionar legenda
    ascii_chart += "\n" + "-" * 50 + "\n"
    ascii_chart += f"Maior valor: {max_val} ({df.loc[df[y_col].idxmax()][x_col]})\n"
    ascii_chart += f"Menor valor: {df[y_col].min()} ({df.loc[df[y_col].idxmin()][x_col]})\n"
    ascii_chart += f"Média: {df[y_col].mean():.2f}\n"
    
    st.code(ascii_chart)
    return True

# Função para criar tabela de dados formatada
def create_ascii_table(df, title):
    st.subheader(title)
    
    # Criar cabeçalho
    headers = df.columns
    col_widths = [max(len(str(x)) for x in df[col].tolist() + [col]) + 2 for col in headers]
    
    # Linha de cabeçalho
    header_row = "| " + " | ".join(f"{h:<{col_widths[i]}}" for i, h in enumerate(headers)) + " |"
    separator = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    
    # Linhas de dados
    data_rows = []
    for _, row in df.iterrows():
        data_row = "| " + " | ".join(f"{str(row[h]):<{col_widths[i]}}" for i, h in enumerate(headers)) + " |"
        data_rows.append(data_row)
    
    # Montar tabela
    ascii_table = separator + "\n" + header_row + "\n" + separator + "\n"
    ascii_table += "\n".join(data_rows) + "\n" + separator
    
    st.code(ascii_table)
    return True

# Função para criar gráfico de pizza ASCII
def create_ascii_pie(df, category_col, value_col, title):
    st.subheader(title)
    
    total = df[value_col].sum()
    
    ascii_pie = f"Gráfico de Pizza: {title}\n\n"
    
    for i, row in df.iterrows():
        category = row[category_col]
        value = row[value_col]
        percentage = (value / total) * 100
        
        # Criar representação visual
        bar_length = int(percentage / 2)  # Cada caractere representa 2%
        ascii_pie += f"{category:<10} | {'■' * bar_length} {percentage:.1f}% (Valor: {value})\n"
    
    st.code(ascii_pie)
    return True

# Função para criar gráfico de linha ASCII
def create_ascii_line(df, x_col, y_col, title, height=15):
    st.subheader(title)
    
    # Preparar dados
    x_values = df[x_col].tolist()
    y_values = df[y_col].tolist()
    
    # Normalizar para altura do gráfico
    min_y = min(y_values)
    max_y = max(y_values)
    range_y = max_y - min_y
    
    if range_y == 0:  # Evitar divisão por zero
        range_y = 1
    
    # Criar gráfico
    ascii_line = f"Gráfico de Linha: {title}\n\n"
    
    # Criar linhas do gráfico (de cima para baixo)
    for h in range(height, -1, -1):
        line = ""
        for y in y_values:
            normalized_y = (y - min_y) / range_y * height if range_y > 0 else 0
            if round(normalized_y) == h:
                line += "o "  # Ponto de dados
            elif h == 0:
                line += "- "  # Linha base
            else:
                line += "  "  # Espaço vazio
        
        # Adicionar escala Y no lado esquerdo
        if h == height:
            y_label = f"{max_y:.1f} "
        elif h == 0:
            y_label = f"{min_y:.1f} "
        elif h == height // 2:
            mid_y = min_y + range_y / 2
            y_label = f"{mid_y:.1f} "
        else:
            y_label = "    "
        
        ascii_line += y_label + line + "\n"
    
    # Adicionar rótulos X
    x_labels = ""
    for x in x_values:
        x_labels += f"{str(x)[:4]:<4}"
    
    ascii_line += "    " + x_labels
    
    st.code(ascii_line)
    return True

# Sidebar
st.sidebar.title("📊 Controles")

# Botão para gerar gráficos
if st.sidebar.button("📊 Gerar Gráficos ASCII", use_container_width=True):
    
    # Gerar dados
    df = generate_simple_data()
    
    # Mostrar dados
    st.subheader("📋 Dados para Visualização")
    st.dataframe(df)
    
    # Criar gráficos ASCII
    st.markdown("---")
    st.subheader("📊 Gráficos ASCII Garantidos")
    
    # Mostrar progresso
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(101):
        progress_bar.progress(i)
        status_text.text(f"Gerando visualizações... {i}%")
        time.sleep(0.01)
    
    status_text.empty()
    progress_bar.empty()
    
    # Criar gráficos ASCII
    create_ascii_chart(df, 'categoria', 'vendas', "Gráfico de Barras ASCII")
    create_ascii_table(df, "Tabela ASCII")
    create_ascii_pie(df, 'categoria', 'vendas', "Gráfico de Pizza ASCII")
    
    # Criar dados para linha
    line_data = pd.DataFrame({
        'mes': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
        'vendas': [5420, 6100, 5800, 7200, 6500, 8000]
    })
    
    create_ascii_line(line_data, 'mes', 'vendas', "Gráfico de Linha ASCII")
    
    st.success("✅ Gráficos ASCII gerados com sucesso!")
    st.balloons()

# Instruções
st.sidebar.markdown("---")
st.sidebar.subheader("📝 Instruções")
st.sidebar.info("""
1. Clique em "Gerar Gráficos ASCII"
2. O sistema criará visualizações em ASCII
3. Funciona em QUALQUER ambiente!
4. Sem dependências externas
""")

# Área principal - Instruções iniciais
if 'button_clicked' not in st.session_state:
    st.markdown("""
    ## 🎯 Sistema de Gráficos ASCII Garantidos
    
    Este sistema foi projetado para funcionar em **QUALQUER** ambiente, mesmo sem bibliotecas gráficas!
    
    ### 🛠️ Características:
    
    - **Zero dependências** além de Streamlit e Pandas
    - Funciona em qualquer ambiente Python
    - Visualizações em ASCII puro
    - Gráficos de barras, pizza e linha
    - Tabelas formatadas
    
    ### 📊 Tipos de gráficos:
    
    1. **Gráficos de Barras ASCII** - Visualização horizontal com caracteres Unicode
    2. **Tabelas ASCII** - Dados formatados em tabela de texto
    3. **Gráficos de Pizza ASCII** - Representação proporcional com caracteres
    4. **Gráficos de Linha ASCII** - Tendências temporais em texto
    
    ### 🚀 Como começar:
    
    Clique no botão **"Gerar Gráficos ASCII"** no menu lateral para começar.
    """)

# Footer
st.markdown("---")
st.markdown("📊 **Sistema de Gráficos ASCII Garantidos** - Funciona em QUALQUER lugar!")
