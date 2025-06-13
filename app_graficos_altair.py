import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Configuração da página
st.set_page_config(
    page_title="DataInsight AI - Gráficos Altair",
    page_icon="📊",
    layout="wide"
)

# Título
st.title("📊 DataInsight AI - Gráficos Altair")
st.markdown("### Versão com gráficos Altair (nativo do Streamlit)")

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

# Função para criar gráficos com Altair
def create_altair_charts(df):
    """Cria gráficos usando Altair (nativo do Streamlit)"""
    try:
        # 1. Gráfico de Barras - Vendas por Região
        if 'vendas' in df.columns and 'regiao' in df.columns:
            st.write("### 1. Gráfico de Barras - Vendas por Região")
            
            # Agregar dados
            vendas_regiao = df.groupby('regiao')['vendas'].sum().reset_index()
            
            # Criar gráfico Altair
            chart1 = alt.Chart(vendas_regiao).mark_bar().encode(
                x='regiao:N',
                y='vendas:Q',
                color='regiao:N',
                tooltip=['regiao', 'vendas']
            ).properties(
                title='Vendas por Região',
                height=400
            )
            
            # Exibir gráfico
            st.altair_chart(chart1, use_container_width=True)
            
            # Mostrar dados usados
            with st.expander("Ver dados do gráfico"):
                st.dataframe(vendas_regiao)
        
        # 2. Gráfico de Pizza (Donut) - Distribuição por Produto
        if 'produto' in df.columns:
            st.write("### 2. Gráfico de Donut - Distribuição por Produto")
            
            # Agregar dados
            produto_counts = df['produto'].value_counts().reset_index()
            produto_counts.columns = ['produto', 'contagem']
            
            # Criar gráfico Altair (donut chart)
            chart2 = alt.Chart(produto_counts).mark_arc(innerRadius=50).encode(
                theta='contagem:Q',
                color='produto:N',
                tooltip=['produto', 'contagem']
            ).properties(
                title='Distribuição por Produto',
                height=400
            )
            
            # Exibir gráfico
            st.altair_chart(chart2, use_container_width=True)
            
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
            vendas_mes['ordem'] = vendas_mes['mes'].apply(lambda x: meses_ordem.index(x) if x in meses_ordem else 999)
            vendas_mes = vendas_mes.sort_values('ordem')
            
            # Criar gráfico Altair
            chart3 = alt.Chart(vendas_mes).mark_line(point=True).encode(
                x=alt.X('mes:N', sort=meses_ordem),
                y='vendas:Q',
                tooltip=['mes', 'vendas']
            ).properties(
                title='Vendas por Mês',
                height=400
            )
            
            # Exibir gráfico
            st.altair_chart(chart3, use_container_width=True)
            
            # Mostrar dados usados
            with st.expander("Ver dados do gráfico"):
                st.dataframe(vendas_mes[['mes', 'vendas']])
        
        # 4. Scatter Plot - Vendas vs Satisfação
        if 'vendas' in df.columns and 'satisfacao' in df.columns:
            st.write("### 4. Scatter Plot - Vendas vs Satisfação")
            
            # Criar gráfico Altair
            chart4 = alt.Chart(df).mark_circle(size=60).encode(
                x='satisfacao:Q',
                y='vendas:Q',
                color='regiao:N',
                tooltip=['satisfacao', 'vendas', 'regiao']
            ).properties(
                title='Vendas vs Satisfação',
                height=400
            )
            
            # Exibir gráfico
            st.altair_chart(chart4, use_container_width=True)
            
            # Mostrar dados usados
            with st.expander("Ver dados do gráfico"):
                st.dataframe(df[['satisfacao', 'vendas', 'regiao']].head(10))
        
        # 5. Histograma - Distribuição de Vendas
        if 'vendas' in df.columns:
            st.write("### 5. Histograma - Distribuição de Vendas")
            
            # Criar gráfico Altair
            chart5 = alt.Chart(df).mark_bar().encode(
                alt.X('vendas:Q', bin=alt.Bin(maxbins=20), title='Vendas'),
                y='count()',
                tooltip=['count()']
            ).properties(
                title='Distribuição de Vendas',
                height=400
            )
            
            # Exibir gráfico
            st.altair_chart(chart5, use_container_width=True)
            
            # Mostrar dados usados
            with st.expander("Ver estatísticas da distribuição"):
                st.write(df['vendas'].describe())
        
        # 6. Gráfico de Barras Horizontais - Top Produtos por Lucro
        if 'produto' in df.columns and 'lucro' in df.columns:
            st.write("### 6. Gráfico de Barras Horizontais - Top Produtos por Lucro")
            
            # Agregar dados
            lucro_produto = df.groupby('produto')['lucro'].sum().reset_index()
            
            # Criar gráfico Altair
            chart6 = alt.Chart(lucro_produto).mark_bar().encode(
                y=alt.Y('produto:N', sort='-x'),
                x='lucro:Q',
                color='produto:N',
                tooltip=['produto', 'lucro']
            ).properties(
                title='Lucro por Produto',
                height=400
            )
            
            # Exibir gráfico
            st.altair_chart(chart6, use_container_width=True)
            
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
    if st.button("🎨 Gerar Gráficos Altair", type="primary", use_container_width=True):
        with st.spinner("Gerando gráficos..."):
            # Criar gráficos
            success = create_altair_charts(df)
            
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
    3. Clique no botão **Gerar Gráficos Altair**
    4. Veja os 6 tipos diferentes de gráficos
    
    ### Gráficos disponíveis:
    - Gráfico de Barras - Vendas por Região
    - Gráfico de Donut - Distribuição por Produto
    - Gráfico de Linha - Vendas por Mês
    - Scatter Plot - Vendas vs Satisfação
    - Histograma - Distribuição de Vendas
    - Gráfico de Barras Horizontais - Top Produtos por Lucro
    """)

# Footer
st.markdown("---")
st.markdown("📊 **DataInsight AI** - Versão com Gráficos Altair (nativo do Streamlit)")
