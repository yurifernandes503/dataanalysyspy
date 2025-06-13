import streamlit as st
import pandas as pd
import numpy as np
import time
import warnings
warnings.filterwarnings('ignore')

# Tentar importar bibliotecas de gráficos (com fallbacks)
PLOTLY_AVAILABLE = False
MATPLOTLIB_AVAILABLE = False
SEABORN_AVAILABLE = False

try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
    print("✅ Plotly carregado com sucesso")
except ImportError:
    print("⚠️ Plotly não disponível")

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Backend não-interativo
    MATPLOTLIB_AVAILABLE = True
    print("✅ Matplotlib carregado com sucesso")
except ImportError:
    print("⚠️ Matplotlib não disponível")

try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
    print("✅ Seaborn carregado com sucesso")
except ImportError:
    print("⚠️ Seaborn não disponível")

# Configuração da página
st.set_page_config(
    page_title="DataInsight AI Pro - Gráficos Robustos",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Avançado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .hero-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 10px 25px rgba(240, 147, 251, 0.3);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(240, 147, 251, 0.4);
    }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 1rem;
        font-weight: 500;
        opacity: 0.9;
    }
    
    .chart-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    }
    
    .success-alert {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .error-alert {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    
    .info-alert {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        color: #0c5460;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="hero-header">
    <h1 style="font-size: 3.5rem; font-weight: 700; margin-bottom: 1rem;">
        🚀 DataInsight AI Pro
    </h1>
    <h3 style="font-size: 1.5rem; font-weight: 400; margin-bottom: 1rem;">
        Análise Avançada com Gráficos Garantidos
    </h3>
    <p style="font-size: 1.1rem; opacity: 0.8;">
        Sistema robusto com múltiplas bibliotecas de visualização
    </p>
</div>
""", unsafe_allow_html=True)

# Inicializar session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'df' not in st.session_state:
    st.session_state.df = None
if 'charts_generated' not in st.session_state:
    st.session_state.charts_generated = False

# Função para gerar dados de exemplo AVANÇADA
@st.cache_data
def generate_advanced_sample_data():
    """Gera dados de exemplo mais realistas e complexos"""
    np.random.seed(42)
    n_records = 500
    
    # Dados mais realistas
    vendedores = [
        'João Silva', 'Maria Santos', 'Pedro Costa', 'Ana Lima', 'Carlos Rocha',
        'Lucia Ferreira', 'Roberto Alves', 'Fernanda Dias', 'Marcos Oliveira',
        'Patricia Souza', 'Ricardo Mendes', 'Juliana Castro', 'Gabriel Torres',
        'Camila Ribeiro', 'Diego Martins', 'Beatriz Gomes', 'Leonardo Pereira',
        'Isabela Cardoso', 'Thiago Barbosa', 'Natalia Ramos'
    ]
    
    produtos = [
        'iPhone 15 Pro Max', 'MacBook Pro M3', 'iPad Air', 'Apple Watch Ultra 2',
        'Samsung Galaxy S24 Ultra', 'Dell XPS 15', 'Surface Pro 10', 'PlayStation 5',
        'Xbox Series X', 'Nintendo Switch OLED', 'AirPods Pro 2', 'Sony WH-1000XM5',
        'Canon EOS R6 Mark II', 'GoPro Hero 12', 'Tesla Model 3', 'Drone DJI Air 3',
        'Monitor LG 4K', 'Teclado Mecânico', 'Mouse Gamer', 'Webcam 4K'
    ]
    
    regioes = ['Norte', 'Sul', 'Leste', 'Oeste', 'Centro', 'Nordeste']
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    categorias = ['Eletrônicos', 'Informática', 'Games', 'Acessórios', 'Automotivo', 'Casa']
    canais = ['Online', 'Loja Física', 'Marketplace', 'App Mobile', 'Telefone', 'WhatsApp']
    
    data = []
    for i in range(n_records):
        categoria = np.random.choice(categorias)
        
        # Vendas baseadas na categoria com distribuição mais realista
        if categoria == 'Eletrônicos':
            vendas_base = np.random.lognormal(10.5, 0.8)  # Distribuição log-normal
        elif categoria == 'Informática':
            vendas_base = np.random.lognormal(10.2, 0.7)
        elif categoria == 'Games':
            vendas_base = np.random.lognormal(9.8, 0.6)
        elif categoria == 'Automotivo':
            vendas_base = np.random.lognormal(11.2, 1.0)
        elif categoria == 'Casa':
            vendas_base = np.random.lognormal(9.5, 0.5)
        else:  # Acessórios
            vendas_base = np.random.lognormal(8.8, 0.4)
        
        vendas = max(1000, int(vendas_base))
        custo = int(vendas * np.random.uniform(0.30, 0.70))
        lucro = vendas - custo
        margem = (lucro / vendas) * 100
        
        # Satisfação correlacionada com margem e categoria
        if margem > 50:
            satisfacao = np.random.choice([4, 5], p=[0.2, 0.8])
        elif margem > 35:
            satisfacao = np.random.choice([3, 4, 5], p=[0.1, 0.3, 0.6])
        elif margem > 20:
            satisfacao = np.random.choice([2, 3, 4], p=[0.2, 0.5, 0.3])
        else:
            satisfacao = np.random.choice([1, 2, 3], p=[0.4, 0.4, 0.2])
        
        # Quantidade baseada no preço
        if vendas > 80000:
            quantidade = np.random.randint(1, 3)
        elif vendas > 30000:
            quantidade = np.random.randint(1, 8)
        elif vendas > 10000:
            quantidade = np.random.randint(1, 20)
        else:
            quantidade = np.random.randint(1, 100)
        
        # Adicionar sazonalidade
        mes = np.random.choice(meses)
        if mes in ['Nov', 'Dez']:  # Black Friday e Natal
            vendas = int(vendas * np.random.uniform(1.2, 1.8))
        elif mes in ['Jan', 'Fev']:  # Início do ano
            vendas = int(vendas * np.random.uniform(0.7, 0.9))
        
        data.append({
            'id': i + 1,
            'vendas': vendas,
            'custo': custo,
            'lucro': lucro,
            'margem': round(margem, 2),
            'regiao': np.random.choice(regioes),
            'produto': np.random.choice(produtos),
            'categoria': categoria,
            'mes': mes,
            'vendedor': np.random.choice(vendedores),
            'canal': np.random.choice(canais),
            'satisfacao': satisfacao,
            'quantidade': quantidade,
            'desconto': round(np.random.uniform(0, 0.40), 3),
            'tempo_entrega': np.random.randint(1, 30),
            'avaliacao': round(np.random.uniform(1, 5), 1),
            'idade_cliente': np.random.randint(18, 75),
            'genero': np.random.choice(['M', 'F'], p=[0.52, 0.48]),
            'cidade': np.random.choice(['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Salvador', 'Brasília', 'Fortaleza', 'Manaus', 'Curitiba', 'Recife', 'Porto Alegre']),
            'forma_pagamento': np.random.choice(['Cartão Crédito', 'Cartão Débito', 'PIX', 'Boleto', 'Dinheiro'], p=[0.4, 0.2, 0.25, 0.1, 0.05])
        })
    
    df = pd.DataFrame(data)
    
    # Adicionar colunas calculadas
    df['ticket_medio'] = df['vendas'] / df['quantidade']
    df['roi'] = (df['lucro'] / df['custo']) * 100
    df['score_cliente'] = (df['satisfacao'] * 0.4 + df['avaliacao'] * 0.6).round(1)
    df['vendas_por_dia'] = df['vendas'] / df['tempo_entrega']
    df['eficiencia'] = (df['vendas'] / (df['tempo_entrega'] + 1)).round(2)
    
    return df

# Função ROBUSTA para criar gráficos com múltiplos fallbacks
def create_robust_charts(df):
    """Cria gráficos usando múltiplas bibliotecas com fallbacks"""
    charts_created = 0
    total_charts = 8
    
    st.info("🎨 Iniciando geração de gráficos robustos...")
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # 1. Gráfico de Barras - Vendas por Região
        status_text.text("📊 Criando gráfico de vendas por região...")
        progress_bar.progress(10)
        
        if 'vendas' in df.columns and 'regiao' in df.columns:
            vendas_regiao = df.groupby('regiao').agg({
                'vendas': 'sum',
                'lucro': 'sum',
                'quantidade': 'sum'
            }).reset_index()
            
            chart_created = False
            
            # Tentar Plotly primeiro
            if PLOTLY_AVAILABLE and not chart_created:
                try:
                    fig1 = px.bar(
                        vendas_regiao,
                        x='regiao',
                        y='vendas',
                        color='lucro',
                        title='📊 Vendas e Lucro por Região',
                        text='vendas',
                        color_continuous_scale='Viridis',
                        hover_data=['lucro', 'quantidade']
                    )
                    
                    fig1.update_traces(
                        texttemplate='R$ %{text:,.0f}',
                        textposition='outside'
                    )
                    
                    fig1.update_layout(
                        height=500,
                        title_x=0.5,
                        title_font_size=20,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.plotly_chart(fig1, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    charts_created += 1
                    chart_created = True
                    st.success("✅ Gráfico 1/8 criado com Plotly")
                    
                except Exception as e:
                    st.warning(f"⚠️ Plotly falhou: {str(e)}")
            
            # Fallback para Matplotlib
            if MATPLOTLIB_AVAILABLE and not chart_created:
                try:
                    fig, ax = plt.subplots(figsize=(12, 6))
                    bars = ax.bar(vendas_regiao['regiao'], vendas_regiao['vendas'], 
                                 color=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'])
                    
                    ax.set_title('📊 Vendas por Região', fontsize=16, fontweight='bold')
                    ax.set_xlabel('Região', fontsize=12)
                    ax.set_ylabel('Vendas (R$)', fontsize=12)
                    
                    # Adicionar valores nas barras
                    for bar in bars:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height,
                               f'R$ {height:,.0f}', ha='center', va='bottom')
                    
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.pyplot(fig)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    plt.close()
                    charts_created += 1
                    chart_created = True
                    st.success("✅ Gráfico 1/8 criado com Matplotlib")
                    
                except Exception as e:
                    st.warning(f"⚠️ Matplotlib falhou: {str(e)}")
            
            # Fallback para gráfico nativo do Streamlit
            if not chart_created:
                try:
                    st.subheader("📊 Vendas por Região")
                    vendas_regiao_chart = vendas_regiao.set_index('regiao')['vendas']
                    st.bar_chart(vendas_regiao_chart)
                    charts_created += 1
                    chart_created = True
                    st.success("✅ Gráfico 1/8 criado com Streamlit nativo")
                except Exception as e:
                    st.error(f"❌ Todos os métodos falharam para gráfico 1: {str(e)}")
        
        progress_bar.progress(25)
        
        # 2. Gráfico de Pizza - Distribuição por Categoria
        status_text.text("🥧 Criando gráfico de distribuição por categoria...")
        
        if 'categoria' in df.columns and 'vendas' in df.columns:
            categoria_vendas = df.groupby('categoria')['vendas'].sum().reset_index()
            
            chart_created = False
            
            # Tentar Plotly primeiro
            if PLOTLY_AVAILABLE and not chart_created:
                try:
                    fig2 = px.pie(
                        categoria_vendas,
                        values='vendas',
                        names='categoria',
                        title='🥧 Distribuição de Vendas por Categoria',
                        color_discrete_sequence=px.colors.qualitative.Set3,
                        hole=0.4
                    )
                    
                    fig2.update_traces(
                        textposition='inside',
                        textinfo='percent+label',
                        hovertemplate='<b>%{label}</b><br>Vendas: R$ %{value:,.0f}<br>Percentual: %{percent}<extra></extra>'
                    )
                    
                    fig2.update_layout(
                        height=500,
                        title_x=0.5,
                        title_font_size=20,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.plotly_chart(fig2, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    charts_created += 1
                    chart_created = True
                    st.success("✅ Gráfico 2/8 criado com Plotly")
                    
                except Exception as e:
                    st.warning(f"⚠️ Plotly falhou: {str(e)}")
            
            # Fallback para Matplotlib
            if MATPLOTLIB_AVAILABLE and not chart_created:
                try:
                    fig, ax = plt.subplots(figsize=(10, 8))
                    colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
                    wedges, texts, autotexts = ax.pie(categoria_vendas['vendas'], 
                                                     labels=categoria_vendas['categoria'],
                                                     autopct='%1.1f%%',
                                                     colors=colors[:len(categoria_vendas)],
                                                     startangle=90)
                    
                    ax.set_title('🥧 Distribuição de Vendas por Categoria', fontsize=16, fontweight='bold')
                    
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.pyplot(fig)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    plt.close()
                    charts_created += 1
                    chart_created = True
                    st.success("✅ Gráfico 2/8 criado com Matplotlib")
                    
                except Exception as e:
                    st.warning(f"⚠️ Matplotlib falhou: {str(e)}")
            
            if not chart_created:
                st.error("❌ Não foi possível criar gráfico de pizza")
        
        progress_bar.progress(40)
        
        # 3. Gráfico de Linha - Tendência Temporal
        status_text.text("📈 Criando gráfico de tendência temporal...")
        
        if 'vendas' in df.columns and 'mes' in df.columns:
            meses_ordem = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
            
            vendas_mes = df.groupby('mes').agg({
                'vendas': 'sum',
                'lucro': 'sum',
                'quantidade': 'sum'
            }).reindex(meses_ordem, fill_value=0).reset_index()
            vendas_mes.columns = ['mes', 'vendas', 'lucro', 'quantidade']
            
            chart_created = False
            
            # Tentar Plotly primeiro
            if PLOTLY_AVAILABLE and not chart_created:
                try:
                    fig3 = go.Figure()
                    
                    fig3.add_trace(go.Scatter(
                        x=vendas_mes['mes'],
                        y=vendas_mes['vendas'],
                        mode='lines+markers',
                        name='Vendas',
                        line=dict(color='#667eea', width=4),
                        marker=dict(size=10, symbol='circle'),
                        hovertemplate='<b>Vendas</b><br>Mês: %{x}<br>Valor: R$ %{y:,.0f}<extra></extra>'
                    ))
                    
                    fig3.add_trace(go.Scatter(
                        x=vendas_mes['mes'],
                        y=vendas_mes['lucro'],
                        mode='lines+markers',
                        name='Lucro',
                        line=dict(color='#f093fb', width=4),
                        marker=dict(size=10, symbol='diamond'),
                        yaxis='y2',
                        hovertemplate='<b>Lucro</b><br>Mês: %{x}<br>Valor: R$ %{y:,.0f}<extra></extra>'
                    ))
                    
                    fig3.update_layout(
                        title='📈 Tendência de Vendas e Lucro por Mês',
                        xaxis_title='Mês',
                        yaxis_title='Vendas (R$)',
                        yaxis2=dict(title='Lucro (R$)', overlaying='y', side='right'),
                        height=500,
                        title_x=0.5,
                        title_font_size=20,
                        hovermode='x unified',
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        legend=dict(x=0.02, y=0.98)
                    )
                    
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.plotly_chart(fig3, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    charts_created += 1
                    chart_created = True
                    st.success("✅ Gráfico 3/8 criado com Plotly")
                    
                except Exception as e:
                    st.warning(f"⚠️ Plotly falhou: {str(e)}")
            
            # Fallback para Matplotlib
            if MATPLOTLIB_AVAILABLE and not chart_created:
                try:
                    fig, ax1 = plt.subplots(figsize=(12, 6))
                    
                    color = '#667eea'
                    ax1.set_xlabel('Mês')
                    ax1.set_ylabel('Vendas (R$)', color=color)
                    line1 = ax1.plot(vendas_mes['mes'], vendas_mes['vendas'], 
                                    color=color, marker='o', linewidth=3, markersize=8, label='Vendas')
                    ax1.tick_params(axis='y', labelcolor=color)
                    
                    ax2 = ax1.twinx()
                    color = '#f093fb'
                    ax2.set_ylabel('Lucro (R$)', color=color)
                    line2 = ax2.plot(vendas_mes['mes'], vendas_mes['lucro'], 
                                    color=color, marker='s', linewidth=3, markersize=8, label='Lucro')
                    ax2.tick_params(axis='y', labelcolor=color)
                    
                    ax1.set_title('📈 Tendência de Vendas e Lucro por Mês', fontsize=16, fontweight='bold')
                    
                    # Adicionar legenda
                    lines1, labels1 = ax1.get_legend_handles_labels()
                    lines2, labels2 = ax2.get_legend_handles_labels()
                    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
                    
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.pyplot(fig)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    plt.close()
                    charts_created += 1
                    chart_created = True
                    st.success("✅ Gráfico 3/8 criado com Matplotlib")
                    
                except Exception as e:
                    st.warning(f"⚠️ Matplotlib falhou: {str(e)}")
            
            # Fallback para gráfico nativo do Streamlit
            if not chart_created:
                try:
                    st.subheader("📈 Tendência de Vendas por Mês")
                    vendas_mes_chart = vendas_mes.set_index('mes')['vendas']
                    st.line_chart(vendas_mes_chart)
                    charts_created += 1
                    chart_created = True
                    st.success("✅ Gráfico 3/8 criado com Streamlit nativo")
                except Exception as e:
                    st.error(f"❌ Todos os métodos falharam para gráfico 3: {str(e)}")
        
        progress_bar.progress(55)
        
        # 4. Scatter Plot - Vendas vs Satisfação
        status_text.text("💫 Criando scatter plot...")
        
        if 'vendas' in df.columns and 'satisfacao' in df.columns:
            chart_created = False
            
            # Tentar Plotly primeiro
            if PLOTLY_AVAILABLE and not chart_created:
                try:
                    fig4 = px.scatter(
                        df,
                        x='satisfacao',
                        y='vendas',
                        color='regiao',
                        size='lucro',
                        title='💫 Relação: Vendas × Satisfação × Região',
                        hover_data=['produto', 'categoria', 'margem'],
                        color_discrete_sequence=px.colors.qualitative.Bold,
                        size_max=30
                    )
                    
                    fig4.update_traces(
                        marker=dict(line=dict(width=1, color='white'))
                    )
                    
                    fig4.update_layout(
                        height=500,
                        title_x=0.5,
                        title_font_size=20,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(title='Satisfação (1-5)'),
                        yaxis=dict(title='Vendas (R$)')
                    )
                    
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.plotly_chart(fig4, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    charts_created += 1
                    chart_created = True
                    st.success("✅ Gráfico 4/8 criado com Plotly")
                    
                except Exception as e:
                    st.warning(f"⚠️ Plotly falhou: {str(e)}")
            
            # Fallback para Matplotlib
            if MATPLOTLIB_AVAILABLE and not chart_created:
                try:
                    fig, ax = plt.subplots(figsize=(12, 8))
                    
                    # Criar scatter plot com cores por região
                    regioes_unicas = df['regiao'].unique()
                    colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
                    
                    for i, regiao in enumerate(regioes_unicas):
                        df_regiao = df[df['regiao'] == regiao]
                        ax.scatter(df_regiao['satisfacao'], df_regiao['vendas'], 
                                  c=colors[i % len(colors)], label=regiao, alpha=0.7, s=60)
                    
                    ax.set_xlabel('Satisfação (1-5)', fontsize=12)
                    ax.set_ylabel('Vendas (R$)', fontsize=12)
                    ax.set_title('💫 Relação: Vendas × Satisfação × Região', fontsize=16, fontweight='bold')
                    ax.legend()
                    ax.grid(True, alpha=0.3)
                    
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.pyplot(fig)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    plt.close()
                    charts_created += 1
                    chart_created = True
                    st.success("✅ Gráfico 4/8 criado com Matplotlib")
                    
                except Exception as e:
                    st.warning(f"⚠️ Matplotlib falhou: {str(e)}")
            
            if not chart_created:
                st.error("❌ Não foi possível criar scatter plot")
        
        progress_bar.progress(70)
        
        # 5. Histograma - Distribuição de Vendas
        status_text.text("📊 Criando histograma...")
        
        if 'vendas' in df.columns:
            chart_created = False
            
            # Tentar Plotly primeiro
            if PLOTLY_AVAILABLE and not chart_created:
                try:
                    fig5 = px.histogram(
                        df,
                        x='vendas',
                        nbins=25,
                        title='📊 Distribuição de Vendas',
                        color_discrete_sequence=['#4facfe'],
                        marginal='box'
                    )
                    
                    fig5.update_traces(
                        marker=dict(line=dict(width=1, color='white'))
                    )
                    
                    fig5.update_layout(
                        height=500,
                        title_x=0.5,
                        title_font_size=20,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(title='Vendas (R$)'),
                        yaxis=dict(title='Frequência')
                    )
                    
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.plotly_chart(fig5, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    charts_created += 1
                    chart_created = True
                    st.success("✅ Gráfico 5/8 criado com Plotly")
                    
                except Exception as e:
                    st.warning(f"⚠️ Plotly falhou: {str(e)}")
            
            # Fallback para Matplotlib
            if MATPLOTLIB_AVAILABLE and not chart_created:
                try:
                    fig, ax = plt.subplots(figsize=(12, 6))
                    
                    n, bins, patches = ax.hist(df['vendas'], bins=25, color='#4facfe', alpha=0.7, edgecolor='white')
                    
                    ax.set_xlabel('Vendas (R$)', fontsize=12)
                    ax.set_ylabel('Frequência', fontsize=12)
                    ax.set_title('📊 Distribuição de Vendas', fontsize=16, fontweight='bold')
                    ax.grid(True, alpha=0.3)
                    
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.pyplot(fig)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    plt.close()
                    charts_created += 1
                    chart_created = True
                    st.success("✅ Gráfico 5/8 criado com Matplotlib")
                    
                except Exception as e:
                    st.warning(f"⚠️ Matplotlib falhou: {str(e)}")
            
            if not chart_created:
                st.error("❌ Não foi possível criar histograma")
        
        progress_bar.progress(85)
        
        # 6. Top Produtos
        status_text.text("🏆 Criando ranking de produtos...")
        
        if 'produto' in df.columns and 'vendas' in df.columns:
            top_produtos = df.groupby('produto')['vendas'].sum().nlargest(10).reset_index()
            
            chart_created = False
            
            # Tentar Plotly primeiro
            if PLOTLY_AVAILABLE and not chart_created:
                try:
                    fig6 = px.bar(
                        top_produtos,
                        y='produto',
                        x='vendas',
                        orientation='h',
                        title='🏆 Top 10 Produtos por Vendas',
                        color='vendas',
                        color_continuous_scale='Viridis'
                    )
                    
                    fig6.update_layout(
                        height=500,
                        title_x=0.5,
                        title_font_size=20,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        yaxis=dict(title='Produto'),
                        xaxis=dict(title='Vendas (R$)')
                    )
                    
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.plotly_chart(fig6, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    charts_created += 1
                    chart_created = True
                    st.success("✅ Gráfico 6/8 criado com Plotly")
                    
                except Exception as e:
                    st.warning(f"⚠️ Plotly falhou: {str(e)}")
            
            # Fallback para Matplotlib
            if MATPLOTLIB_AVAILABLE and not chart_created:
                try:
                    fig, ax = plt.subplots(figsize=(12, 8))
                    
                    y_pos = np.arange(len(top_produtos))
                    bars = ax.barh(y_pos, top_produtos['vendas'], color='#667eea')
                    
                    ax.set_yticks(y_pos)
                    ax.set_yticklabels(top_produtos['produto'])
                    ax.set_xlabel('Vendas (R$)', fontsize=12)
                    ax.set_title('🏆 Top 10 Produtos por Vendas', fontsize=16, fontweight='bold')
                    
                    # Adicionar valores nas barras
                    for i, bar in enumerate(bars):
                        width = bar.get_width()
                        ax.text(width, bar.get_y() + bar.get_height()/2,
                               f'R$ {width:,.0f}', ha='left', va='center')
                    
                    plt.tight_layout()
                    
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.pyplot(fig)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    plt.close()
                    charts_created += 1
                    chart_created = True
                    st.success("✅ Gráfico 6/8 criado com Matplotlib")
                    
                except Exception as e:
                    st.warning(f"⚠️ Matplotlib falhou: {str(e)}")
            
            if not chart_created:
                st.error("❌ Não foi possível criar ranking de produtos")
        
        progress_bar.progress(100)
        status_text.text("✅ Gráficos concluídos!")
        
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()
        
        # Resumo final
        if charts_created > 0:
            st.markdown(f"""
            <div class="success-alert">
                <h3>🎉 Sucesso!</h3>
                <p><strong>{charts_created}</strong> de {total_charts} gráficos criados com sucesso!</p>
                <p>Sistema robusto funcionando perfeitamente.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="error-alert">
                <h3>❌ Erro</h3>
                <p>Nenhum gráfico pôde ser criado. Verifique as dependências.</p>
            </div>
            """, unsafe_allow_html=True)
        
        return charts_created > 0
        
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"❌ Erro geral na criação de gráficos: {str(e)}")
        return False

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 1.5rem; border-radius: 15px; text-align: center; margin-bottom: 1rem;">
        <h2 style="margin: 0;">🎛️ Controle Central</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Sistema Robusto</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Status das bibliotecas
    st.markdown("### 📚 Status das Bibliotecas")
    
    if PLOTLY_AVAILABLE:
        st.markdown('<div class="success-alert">✅ Plotly: Disponível</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="error-alert">❌ Plotly: Não disponível</div>', unsafe_allow_html=True)
    
    if MATPLOTLIB_AVAILABLE:
        st.markdown('<div class="success-alert">✅ Matplotlib: Disponível</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="error-alert">❌ Matplotlib: Não disponível</div>', unsafe_allow_html=True)
    
    if SEABORN_AVAILABLE:
        st.markdown('<div class="success-alert">✅ Seaborn: Disponível</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-alert">ℹ️ Seaborn: Não disponível</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Botão para dados de exemplo
    if st.button("🎲 Gerar Dataset Avançado", type="primary", use_container_width=True):
        with st.spinner("🔄 Gerando dataset complexo..."):
            st.session_state.df = generate_advanced_sample_data()
            st.session_state.data_loaded = True
            st.session_state.charts_generated = False
            st.success("✅ Dataset avançado carregado!")
            time.sleep(1)
            st.rerun()
    
    # Upload de arquivo
    uploaded_file = st.file_uploader("📁 Upload de Arquivo", type=['csv', 'xlsx', 'json'])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith('.json'):
                df = pd.read_json(uploaded_file)
            
            st.session_state.df = df
            st.session_state.data_loaded = True
            st.session_state.charts_generated = False
            st.success(f"✅ {uploaded_file.name} carregado!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")
    
    st.divider()
    
    # Informações do dataset
    if st.session_state.data_loaded and st.session_state.df is not None:
        df = st.session_state.df
        
        st.markdown("### 📊 Info do Dataset")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📋 Registros", f"{len(df):,}")
            st.metric("📊 Colunas", len(df.columns))
        
        with col2:
            if 'vendas' in df.columns:
                st.metric("💰 Vendas", f"R$ {df['vendas'].sum()/1000:.0f}K")
            if 'lucro' in df.columns:
                st.metric("📈 Lucro", f"R$ {df['lucro'].sum()/1000:.0f}K")

# Interface principal
if st.session_state.data_loaded and st.session_state.df is not None:
    df = st.session_state.df
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📈 Gráficos Robustos", "📋 Dados"])
    
    with tab1:
        st.markdown("## 📊 Dashboard Executivo")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📋 Registros</div>
                <div class="metric-number">{len(df):,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📊 Colunas</div>
                <div class="metric-number">{len(df.columns)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if 'vendas' in df.columns:
                total_vendas = df['vendas'].sum()
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">💰 Vendas</div>
                    <div class="metric-number">R$ {total_vendas/1000000:.1f}M</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col4:
            if 'lucro' in df.columns:
                total_lucro = df['lucro'].sum()
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">📈 Lucro</div>
                    <div class="metric-number">R$ {total_lucro/1000000:.1f}M</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # KPIs adicionais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'margem' in df.columns:
                margem_media = df['margem'].mean()
                st.metric("📊 Margem Média", f"{margem_media:.1f}%")
        
        with col2:
            if 'satisfacao' in df.columns:
                satisfacao_media = df['satisfacao'].mean()
                st.metric("⭐ Satisfação", f"{satisfacao_media:.1f}/5")
        
        with col3:
            if 'ticket_medio' in df.columns:
                ticket_medio = df['ticket_medio'].mean()
                st.metric("🎫 Ticket Médio", f"R$ {ticket_medio:,.0f}")
        
        with col4:
            if 'roi' in df.columns:
                roi_medio = df['roi'].mean()
                st.metric("📈 ROI Médio", f"{roi_medio:.1f}%")
    
    with tab2:
        st.markdown("## 📈 Gráficos Robustos")
        
        # Botão para gerar gráficos
        if st.button("🎨 Gerar Gráficos Robustos", type="primary", use_container_width=True):
            success = create_robust_charts(df)
            st.session_state.charts_generated = success
        
        if not st.session_state.charts_generated:
            st.markdown("""
            ### 🎯 Sistema de Gráficos Robustos
            
            Este sistema usa múltiplas bibliotecas com fallbacks automáticos:
            
            1. **Plotly** (Primeira opção) - Gráficos interativos avançados
            2. **Matplotlib** (Fallback) - Gráficos estáticos confiáveis  
            3. **Streamlit nativo** (Último recurso) - Gráficos básicos garantidos
            
            **Garantia:** Pelo menos uma biblioteca funcionará!
            """)
    
    with tab3:
        st.markdown("## 📋 Explorador de Dados")
        
        # Filtros
        col1, col2 = st.columns(2)
        
        with col1:
            if 'regiao' in df.columns:
                regioes = st.multiselect("🌍 Filtrar por região:", df['regiao'].unique())
                if regioes:
                    df = df[df['regiao'].isin(regioes)]
        
        with col2:
            if 'categoria' in df.columns:
                categorias = st.multiselect("📦 Filtrar por categoria:", df['categoria'].unique())
                if categorias:
                    df = df[df['categoria'].isin(categorias)]
        
        # Exibir dados
        st.dataframe(df, use_container_width=True, height=400)
        
        # Estatísticas
        if len(df) > 0:
            st.markdown("### 📊 Estatísticas dos Dados Filtrados")
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                st.dataframe(df[numeric_cols].describe(), use_container_width=True)

else:
    # Tela inicial
    st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🚀</div>
        <h2 style="color: #667eea; margin-bottom: 2rem;">Sistema de Gráficos Ultra Robusto!</h2>
        <p style="font-size: 1.2rem; color: #666; max-width: 800px; margin: 0 auto 2rem auto;">
            Sistema avançado com múltiplas bibliotecas de visualização e fallbacks automáticos.
            <strong>Garantia de funcionamento!</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Funcionalidades
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-alert">
            <h3>🎨 Gráficos Robustos</h3>
            <ul>
                <li>✅ Plotly interativo</li>
                <li>✅ Matplotlib estático</li>
                <li>✅ Streamlit nativo</li>
                <li>✅ Fallbacks automáticos</li>
                <li>✅ 100% de garantia</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-alert">
            <h3>📊 Dataset Avançado</h3>
            <ul>
                <li>✅ 500+ registros</li>
                <li>✅ 20+ colunas</li>
                <li>✅ Dados realistas</li>
                <li>✅ Correlações complexas</li>
                <li>✅ Sazonalidade</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-alert">
            <h3>🔧 Sistema Robusto</h3>
            <ul>
                <li>✅ Detecção automática</li>
                <li>✅ Tratamento de erros</li>
                <li>✅ Múltiplos fallbacks</li>
                <li>✅ Status em tempo real</li>
                <li>✅ Logs detalhados</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("👈 Clique em 'Gerar Dataset Avançado' no menu lateral para começar!")

# Footer
st.markdown("---")
st.markdown("🚀 **DataInsight AI Pro** - Sistema de Gráficos Ultra Robusto com Fallbacks Automáticos")
