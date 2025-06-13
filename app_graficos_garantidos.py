import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# Configuração da página
st.set_page_config(
    page_title="DataInsight AI - Gráficos Garantidos",
    page_icon="📊",
    layout="wide"
)

# Título
st.title("📊 DataInsight AI - Gráficos Garantidos")
st.markdown("### Versão com gráficos 100% funcionais")

# Inicializar session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'df' not in st.session_state:
    st.session_state.df = None

# Função para gerar dados de exemplo
def generate_sample_data():
    """Gera dados de exemplo simples"""
    np.random.seed(42)
    n_records = 100
    
    data = {
        'vendas': np.random.randint(1000, 10000, n_records),
        'regiao': np.random.choice(['Norte', 'Sul', 'Leste', 'Oeste'], n_records),
        'produto': np.random.choice(['Produto A', 'Produto B', 'Produto C'], n_records),
        'mes': np.random.choice(['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'], n_records),
        'satisfacao': np.random.randint(1, 6, n_records),
        'custo': np.random.randint(500, 5000, n_records)
    }
    
    df = pd.DataFrame(data)
    df['lucro'] = df['vendas'] - df['custo']
    
    return df

# Sidebar
with st.sidebar:
    st.header("Controles")
    
    # Botão para dados de exemplo
    if st.button("📊 Carregar Dados de Exemplo", use_container_width=True):
        with st.spinner("Gerando dados..."):
            st.session_state.df = generate_sample_data()
            st.session_state.data_loaded = True
            st.success("✅ Dados carregados!")
            st.rerun()
    
    # Upload de arquivo
    uploaded_file = st.file_uploader("Ou faça upload de um arquivo CSV", type=['csv'])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
            st.session_state.data_loaded = True
            st.success(f"✅ Arquivo carregado: {uploaded_file.name}")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao carregar arquivo: {e}")

# Função para criar gráficos GARANTIDOS
def create_guaranteed_charts(df):
    """Cria gráficos garantidos que funcionam"""
    charts = {}
    
    try:
        # 1. Gráfico de Barras - Vendas por Região
        if 'vendas' in df.columns and 'regiao' in df.columns:
            st.write("### 1. Gráfico de Barras - Vendas por Região")
            
            # Agregar dados
            vendas_regiao = df.groupby('regiao')['vendas'].sum().reset_index()
            
            # Criar figura diretamente com go
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(
                x=vendas_regiao['regiao'],
                y=vendas_regiao['vendas'],
                marker_color='royalblue'
            ))
            
            fig1.update_layout(
                title='Vendas por Região',
                xaxis_title='Região',
                yaxis_title='Vendas',
                height=400
            )
            
            # Exibir gráfico diretamente
            st.plotly_chart(fig1, use_container_width=True)
            
            # Mostrar dados usados
            with st.expander("Ver dados do gráfico"):
                st.dataframe(vendas_regiao)
        
        # 2. Gráfico de Pizza - Distribuição por Produto
        if 'produto' in df.columns:
            st.write("### 2. Gráfico de Pizza - Distribuição por Produto")
            
            # Agregar dados
            produto_counts = df['produto'].value_counts().reset_index()
            produto_counts.columns = ['produto', 'contagem']
            
            # Criar figura diretamente com go
            fig2 = go.Figure(data=[go.Pie(
                labels=produto_counts['produto'],
                values=produto_counts['contagem'],
                hole=.3
            )])
            
            fig2.update_layout(
                title='Distribuição por Produto',
                height=400
            )
            
            # Exibir gráfico diretamente
            st.plotly_chart(fig2, use_container_width=True)
            
            # Mostrar dados usados
            with st.expander("Ver dados do gráfico"):
                st.dataframe(produto_counts)
        
        # 3. Gráfico de Linha - Vendas por Mês
        if 'vendas' in df.columns and 'mes' in df.columns:
            st.write("### 3. Gráfico de Linha - Vendas por Mês")
            
            # Agregar dados
            vendas_mes = df.groupby('mes')['vendas'].sum().reset_index()
            
            # Ordenar meses corretamente
            meses_ordem = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
            vendas_mes['mes'] = pd.Categorical(vendas_mes['mes'], categories=meses_ordem, ordered=True)
            vendas_mes = vendas_mes.sort_values('mes')
            
            # Criar figura diretamente com go
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(
                x=vendas_mes['mes'],
                y=vendas_mes['vendas'],
                mode='lines+markers',
                marker=dict(size=10),
                line=dict(width=4, color='green')
            ))
            
            fig3.update_layout(
                title='Vendas por Mês',
                xaxis_title='Mês',
                yaxis_title='Vendas',
                height=400
            )
            
            # Exibir gráfico diretamente
            st.plotly_chart(fig3, use_container_width=True)
            
            # Mostrar dados usados
            with st.expander("Ver dados do gráfico"):
                st.dataframe(vendas_mes)
        
        # 4. Scatter Plot - Vendas vs Satisfação
        if 'vendas' in df.columns and 'satisfacao' in df.columns:
            st.write("### 4. Scatter Plot - Vendas vs Satisfação")
            
            # Criar figura diretamente com go
            fig4 = go.Figure()
            fig4.add_trace(go.Scatter(
                x=df['satisfacao'],
                y=df['vendas'],
                mode='markers',
                marker=dict(
                    size=10,
                    color=df['satisfacao'],
                    colorscale='Viridis',
                    showscale=True
                )
            ))
            
            fig4.update_layout(
                title='Vendas vs Satisfação',
                xaxis_title='Satisfação',
                yaxis_title='Vendas',
                height=400
            )
            
            # Exibir gráfico diretamente
            st.plotly_chart(fig4, use_container_width=True)
            
            # Mostrar dados usados
            with st.expander("Ver dados do gráfico"):
                st.dataframe(df[['satisfacao', 'vendas']].head(10))
        
        # 5. Histograma - Distribuição de Vendas
        if 'vendas' in df.columns:
            st.write("### 5. Histograma - Distribuição de Vendas")
            
            # Criar figura diretamente com go
            fig5 = go.Figure()
            fig5.add_trace(go.Histogram(
                x=df['vendas'],
                nbinsx=20,
                marker_color='purple'
            ))
            
            fig5.update_layout(
                title='Distribuição de Vendas',
                xaxis_title='Vendas',
                yaxis_title='Frequência',
                height=400
            )
            
            # Exibir gráfico diretamente
            st.plotly_chart(fig5, use_container_width=True)
            
            # Mostrar dados usados
            with st.expander("Ver estatísticas da distribuição"):
                st.write(df['vendas'].describe())
        
        # 6. Gráfico de Barras Horizontais - Top Produtos por Lucro
        if 'produto' in df.columns and 'lucro' in df.columns:
            st.write("### 6. Gráfico de Barras Horizontais - Top Produtos por Lucro")
            
            # Agregar dados
            lucro_produto = df.groupby('produto')['lucro'].sum().reset_index()
            lucro_produto = lucro_produto.sort_values('lucro', ascending=True)
            
            # Criar figura diretamente com go
            fig6 = go.Figure()
            fig6.add_trace(go.Bar(
                y=lucro_produto['produto'],
                x=lucro_produto['lucro'],
                orientation='h',
                marker_color='orange'
            ))
            
            fig6.update_layout(
                title='Lucro por Produto',
                xaxis_title='Lucro',
                yaxis_title='Produto',
                height=400
            )
            
            # Exibir gráfico diretamente
            st.plotly_chart(fig6, use_container_width=True)
            
            # Mostrar dados usados
            with st.expander("Ver dados do gráfico"):
                st.dataframe(lucro_produto)
        
        return True
        
    except Exception as e:
        st.error(f"Erro ao criar gráficos: {str(e)}")
        st.error(f"Tipo do erro: {type(e).__name__}")
        return False

# Interface principal
if st.session_state.data_loaded and st.session_state.df is not None:
    df = st.session_state.df
    
    # Mostrar informações do dataset
    st.header("📊 Dados Carregados")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Registros", len(df))
    with col2:
        st.metric("Total de Colunas", len(df.columns))
    with col3:
        if 'vendas' in df.columns:
            st.metric("Total de Vendas", f"R$ {df['vendas'].sum():,.2f}")
    
    # Mostrar prévia dos dados
    with st.expander("Ver prévia dos dados"):
        st.dataframe(df.head(10))
    
    # Botão para gerar gráficos
    if st.button("🎨 Gerar Gráficos Garantidos", type="primary", use_container_width=True):
        with st.spinner("Gerando gráficos..."):
            # Adicionar um pequeno delay para garantir que o spinner seja exibido
            time.sleep(1)
            
            # Criar gráficos
            success = create_guaranteed_charts(df)
            
            if success:
                st.success("✅ Gráficos gerados com sucesso!")
            else:
                st.error("❌ Erro ao gerar gráficos. Veja os detalhes acima.")
    
else:
    # Tela inicial
    st.info("👈 Clique em 'Carregar Dados de Exemplo' no menu lateral para começar")
    
    # Explicação
    st.markdown("""
    ## Como usar esta aplicação
    
    1. Clique em **Carregar Dados de Exemplo** no menu lateral
    2. Ou faça upload de um arquivo CSV próprio
    3. Clique no botão **Gerar Gráficos Garantidos**
    4. Veja os 6 tipos diferentes de gráficos
    
    ### Gráficos disponíveis:
    - Gráfico de Barras - Vendas por Região
    - Gráfico de Pizza - Distribuição por Produto
    - Gráfico de Linha - Vendas por Mês
    - Scatter Plot - Vendas vs Satisfação
    - Histograma - Distribuição de Vendas
    - Gráfico de Barras Horizontais - Top Produtos por Lucro
    """)
    
    # Exemplo visual
    st.image("https://via.placeholder.com/800x400?text=Exemplos+de+Gr%C3%A1ficos", 
             caption="Exemplos de visualizações disponíveis")

# Footer
st.markdown("---")
st.markdown("📊 **DataInsight AI** - Versão com Gráficos Garantidos")
