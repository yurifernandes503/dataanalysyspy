import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração da página
st.set_page_config(
    page_title="DataInsight AI - Gráficos Simples",
    page_icon="📊",
    layout="wide"
)

# Título
st.title("📊 DataInsight AI - Gráficos Simples")
st.markdown("### Versão com gráficos Matplotlib/Seaborn")

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

# Função para criar gráficos com Matplotlib/Seaborn
def create_matplotlib_charts(df):
    """Cria gráficos usando Matplotlib e Seaborn"""
    try:
        # 1. Gráfico de Barras - Vendas por Região
        if 'vendas' in df.columns and 'regiao' in df.columns:
            st.write("### 1. Gráfico de Barras - Vendas por Região")
            
            # Agregar dados
            vendas_regiao = df.groupby('regiao')['vendas'].sum().reset_index()
            
            # Criar figura
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x='regiao', y='vendas', data=vendas_regiao, ax=ax)
            ax.set_title('Vendas por Região')
            ax.set_xlabel('Região')
            ax.set_ylabel('Vendas')
            
            # Exibir gráfico
            st.pyplot(fig)
            
            # Mostrar dados usados
            with st.expander("Ver dados do gráfico"):
                st.dataframe(vendas_regiao)
        
        # 2. Gráfico de Pizza - Distribuição por Produto
        if 'produto' in df.columns:
            st.write("### 2. Gráfico de Pizza - Distribuição por Produto")
            
            # Agregar dados
            produto_counts = df['produto'].value_counts()
            
            # Criar figura
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.pie(produto_counts, labels=produto_counts.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            ax.set_title('Distribuição por Produto')
            
            # Exibir gráfico
            st.pyplot(fig)
            
            # Mostrar dados usados
            with st.expander("Ver dados do gráfico"):
                st.dataframe(produto_counts.reset_index())
        
        # 3. Gráfico de Linha - Vendas por Mês
        if 'vendas' in df.columns and 'mes' in df.columns:
            st.write("### 3. Gráfico de Linha - Vendas por Mês")
            
            # Agregar dados
            vendas_mes = df.groupby('mes')['vendas'].sum().reset_index()
            
            # Ordenar meses corretamente
            meses_ordem = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
            vendas_mes['mes'] = pd.Categorical(vendas_mes['mes'], categories=meses_ordem, ordered=True)
            vendas_mes = vendas_mes.sort_values('mes')
            
            # Criar figura
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.lineplot(x='mes', y='vendas', data=vendas_mes, marker='o', ax=ax)
            ax.set_title('Vendas por Mês')
            ax.set_xlabel('Mês')
            ax.set_ylabel('Vendas')
            
            # Exibir gráfico
            st.pyplot(fig)
            
            # Mostrar dados usados
            with st.expander("Ver dados do gráfico"):
                st.dataframe(vendas_mes)
        
        # 4. Scatter Plot - Vendas vs Satisfação
        if 'vendas' in df.columns and 'satisfacao' in df.columns:
            st.write("### 4. Scatter Plot - Vendas vs Satisfação")
            
            # Criar figura
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.scatterplot(x='satisfacao', y='vendas', data=df, hue='regiao', size='vendas', sizes=(20, 200), ax=ax)
            ax.set_title('Vendas vs Satisfação')
            ax.set_xlabel('Satisfação')
            ax.set_ylabel('Vendas')
            
            # Exibir gráfico
            st.pyplot(fig)
            
            # Mostrar dados usados
            with st.expander("Ver dados do gráfico"):
                st.dataframe(df[['satisfacao', 'vendas', 'regiao']].head(10))
        
        # 5. Histograma - Distribuição de Vendas
        if 'vendas' in df.columns:
            st.write("### 5. Histograma - Distribuição de Vendas")
            
            # Criar figura
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(df['vendas'], bins=20, kde=True, ax=ax)
            ax.set_title('Distribuição de Vendas')
            ax.set_xlabel('Vendas')
            ax.set_ylabel('Frequência')
            
            # Exibir gráfico
            st.pyplot(fig)
            
            # Mostrar dados usados
            with st.expander("Ver estatísticas da distribuição"):
                st.write(df['vendas'].describe())
        
        # 6. Gráfico de Barras Horizontais - Top Produtos por Lucro
        if 'produto' in df.columns and 'lucro' in df.columns:
            st.write("### 6. Gráfico de Barras Horizontais - Top Produtos por Lucro")
            
            # Agregar dados
            lucro_produto = df.groupby('produto')['lucro'].sum().reset_index()
            lucro_produto = lucro_produto.sort_values('lucro')
            
            # Criar figura
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(y='produto', x='lucro', data=lucro_produto, ax=ax)
            ax.set_title('Lucro por Produto')
            ax.set_xlabel('Lucro')
            ax.set_ylabel('Produto')
            
            # Exibir gráfico
            st.pyplot(fig)
            
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
    if st.button("🎨 Gerar Gráficos Matplotlib/Seaborn", type="primary", use_container_width=True):
        with st.spinner("Gerando gráficos..."):
            # Criar gráficos
            success = create_matplotlib_charts(df)
            
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
    3. Clique no botão **Gerar Gráficos Matplotlib/Seaborn**
    4. Veja os 6 tipos diferentes de gráficos
    
    ### Gráficos disponíveis:
    - Gráfico de Barras - Vendas por Região
    - Gráfico de Pizza - Distribuição por Produto
    - Gráfico de Linha - Vendas por Mês
    - Scatter Plot - Vendas vs Satisfação
    - Histograma - Distribuição de Vendas
    - Gráfico de Barras Horizontais - Top Produtos por Lucro
    """)

# Footer
st.markdown("---")
st.markdown("📊 **DataInsight AI** - Versão com Gráficos Matplotlib/Seaborn")
