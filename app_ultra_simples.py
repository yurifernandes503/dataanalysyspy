import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="DataInsight AI - Versão Ultra Simples",
    page_icon="📊",
    layout="wide"
)

# Título
st.title("📊 DataInsight AI - Versão Ultra Simples")
st.markdown("### Versão sem erros garantida")

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
        st.session_state.df = generate_sample_data()
        st.success("✅ Dados carregados!")
        st.rerun()
    
    # Upload de arquivo
    uploaded_file = st.file_uploader("Ou faça upload de um arquivo CSV", type=['csv'])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
            st.success(f"✅ Arquivo carregado: {uploaded_file.name}")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao carregar arquivo: {e}")

# Inicializar session state
if 'df' not in st.session_state:
    st.session_state.df = None

# Interface principal
if st.session_state.df is not None:
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
    st.subheader("Prévia dos Dados")
    st.dataframe(df.head(10))
    
    # Estatísticas básicas
    st.subheader("Estatísticas Básicas")
    if 'vendas' in df.columns:
        st.write(f"**Média de Vendas:** R$ {df['vendas'].mean():.2f}")
        st.write(f"**Máximo de Vendas:** R$ {df['vendas'].max():.2f}")
        st.write(f"**Mínimo de Vendas:** R$ {df['vendas'].min():.2f}")
    
    # Gráficos nativos do Streamlit (sem bibliotecas externas)
    st.subheader("Visualizações Nativas do Streamlit")
    
    # 1. Gráfico de barras nativo
    if 'regiao' in df.columns and 'vendas' in df.columns:
        st.subheader("Vendas por Região")
        vendas_regiao = df.groupby('regiao')['vendas'].sum()
        st.bar_chart(vendas_regiao)
    
    # 2. Gráfico de linha nativo
    if 'mes' in df.columns and 'vendas' in df.columns:
        st.subheader("Vendas por Mês")
        vendas_mes = df.groupby('mes')['vendas'].sum().reset_index()
        meses_ordem = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        vendas_mes['ordem'] = vendas_mes['mes'].apply(lambda x: meses_ordem.index(x) if x in meses_ordem else 999)
        vendas_mes = vendas_mes.sort_values('ordem')
        chart_data = pd.DataFrame(vendas_mes[['mes', 'vendas']].set_index('mes'))
        st.line_chart(chart_data)
    
    # 3. Tabela de dados agrupados
    if 'produto' in df.columns and 'vendas' in df.columns:
        st.subheader("Vendas por Produto")
        vendas_produto = df.groupby('produto').agg({
            'vendas': 'sum',
            'lucro': 'sum' if 'lucro' in df.columns else None
        }).reset_index()
        st.dataframe(vendas_produto)
    
else:
    # Tela inicial
    st.info("👈 Clique em 'Carregar Dados de Exemplo' no menu lateral para começar")
    
    # Explicação
    st.markdown("""
    ## Como usar esta aplicação
    
    1. Clique em **Carregar Dados de Exemplo** no menu lateral
    2. Ou faça upload de um arquivo CSV próprio
    3. Veja as estatísticas e gráficos nativos do Streamlit
    
    ### Funcionalidades:
    - Visualização de dados
    - Estatísticas básicas
    - Gráficos nativos do Streamlit
    - Sem dependências externas
    """)

# Footer
st.markdown("---")
st.markdown("📊 **DataInsight AI** - Versão Ultra Simples")
