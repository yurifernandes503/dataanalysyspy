import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import google.generativeai as genai
import os
import json
from datetime import datetime
import warnings
import time
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="DataInsight AI Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Ultra Melhorado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        padding-top: 0rem;
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .hero-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="75" cy="75" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="50" cy="10" r="0.5" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.3;
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
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
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(240, 147, 251, 0.4);
    }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-label {
        font-size: 1rem;
        font-weight: 500;
        opacity: 0.9;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(79, 172, 254, 0.3);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .chart-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .status-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(168, 237, 234, 0.3);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .stSelectbox > div > div {
        background: white;
        border-radius: 10px;
        border: 2px solid #e1e5e9;
    }
    
    .stTextArea > div > div > textarea {
        background: white;
        border-radius: 10px;
        border: 2px solid #e1e5e9;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 15px;
        padding: 1rem;
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
    
    .warning-alert {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        color: #856404;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ffc107;
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
    
    /* Animações */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Responsividade */
    @media (max-width: 768px) {
        .hero-header {
            padding: 2rem 1rem;
        }
        .metric-card {
            margin: 0.25rem;
            padding: 1.5rem;
        }
        .metric-number {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'df' not in st.session_state:
    st.session_state.df = None
if 'charts_generated' not in st.session_state:
    st.session_state.charts_generated = False

# Header Ultra Melhorado
st.markdown("""
<div class="hero-header">
    <div class="hero-content">
        <h1 style="font-size: 3.5rem; font-weight: 700; margin-bottom: 1rem; text-shadow: 0 4px 8px rgba(0,0,0,0.2);">
            🚀 DataInsight AI Pro
        </h1>
        <h3 style="font-size: 1.5rem; font-weight: 400; margin-bottom: 1rem; opacity: 0.9;">
            Análise Inteligente de Dados com IA Avançada
        </h3>
        <p style="font-size: 1.1rem; opacity: 0.8; max-width: 600px; margin: 0 auto;">
            Transforme seus dados em insights poderosos com visualizações interativas e análise de IA de última geração
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Configuração do Gemini AI
@st.cache_resource
def configure_gemini():
    """Configura a API do Gemini com cache"""
    try:
        api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            return True, "🟢 Conectado"
        return False, "🔴 Chave API não encontrada"
    except Exception as e:
        return False, f"🔴 Erro: {str(e)}"

# Função para gerar dados de exemplo MELHORADA
@st.cache_data
def generate_sample_data():
    """Gera dados de exemplo mais realistas"""
    np.random.seed(42)
    n_records = 300
    
    # Dados mais realistas
    vendedores = [
        'João Silva', 'Maria Santos', 'Pedro Costa', 'Ana Lima', 'Carlos Rocha',
        'Lucia Ferreira', 'Roberto Alves', 'Fernanda Dias', 'Marcos Oliveira',
        'Patricia Souza', 'Ricardo Mendes', 'Juliana Castro', 'Gabriel Torres',
        'Camila Ribeiro', 'Diego Martins', 'Beatriz Gomes'
    ]
    
    produtos = [
        'iPhone 15 Pro', 'MacBook Air M2', 'iPad Pro', 'Apple Watch Ultra',
        'Samsung Galaxy S24', 'Dell XPS 13', 'Surface Pro 9', 'PlayStation 5',
        'Xbox Series X', 'Nintendo Switch', 'AirPods Pro', 'Sony WH-1000XM5',
        'Canon EOS R6', 'GoPro Hero 12', 'Tesla Model Y', 'Drone DJI Mini 4'
    ]
    
    regioes = ['Norte', 'Sul', 'Leste', 'Oeste', 'Centro']
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    categorias = ['Eletrônicos', 'Informática', 'Games', 'Acessórios', 'Automotivo']
    canais = ['Online', 'Loja Física', 'Marketplace', 'App Mobile', 'Telefone']
    
    data = []
    for i in range(n_records):
        categoria = np.random.choice(categorias)
        
        # Vendas baseadas na categoria
        if categoria == 'Eletrônicos':
            vendas_base = np.random.normal(45000, 15000)
        elif categoria == 'Informática':
            vendas_base = np.random.normal(35000, 12000)
        elif categoria == 'Games':
            vendas_base = np.random.normal(25000, 8000)
        elif categoria == 'Automotivo':
            vendas_base = np.random.normal(85000, 25000)
        else:
            vendas_base = np.random.normal(15000, 5000)
        
        vendas = max(2000, int(vendas_base))
        custo = int(vendas * np.random.uniform(0.35, 0.65))
        lucro = vendas - custo
        margem = (lucro / vendas) * 100
        
        # Satisfação correlacionada com margem e categoria
        if margem > 45:
            satisfacao = np.random.choice([4, 5], p=[0.2, 0.8])
        elif margem > 30:
            satisfacao = np.random.choice([3, 4, 5], p=[0.1, 0.4, 0.5])
        elif margem > 15:
            satisfacao = np.random.choice([2, 3, 4], p=[0.2, 0.5, 0.3])
        else:
            satisfacao = np.random.choice([1, 2, 3], p=[0.4, 0.4, 0.2])
        
        # Quantidade baseada no preço
        if vendas > 50000:
            quantidade = np.random.randint(1, 5)
        elif vendas > 20000:
            quantidade = np.random.randint(1, 15)
        else:
            quantidade = np.random.randint(1, 50)
        
        data.append({
            'id': i + 1,
            'vendas': vendas,
            'custo': custo,
            'lucro': lucro,
            'margem': round(margem, 2),
            'regiao': np.random.choice(regioes),
            'produto': np.random.choice(produtos),
            'categoria': categoria,
            'mes': np.random.choice(meses),
            'vendedor': np.random.choice(vendedores),
            'canal': np.random.choice(canais),
            'satisfacao': satisfacao,
            'quantidade': quantidade,
            'desconto': round(np.random.uniform(0, 0.35), 3),
            'tempo_entrega': np.random.randint(1, 21),
            'avaliacao': round(np.random.uniform(1, 5), 1),
            'idade_cliente': np.random.randint(18, 70),
            'genero': np.random.choice(['M', 'F'], p=[0.52, 0.48])
        })
    
    df = pd.DataFrame(data)
    
    # Adicionar colunas calculadas
    df['ticket_medio'] = df['vendas'] / df['quantidade']
    df['roi'] = (df['lucro'] / df['custo']) * 100
    df['score_cliente'] = (df['satisfacao'] * 0.4 + df['avaliacao'] * 0.6).round(1)
    
    return df

# Função ULTRA MELHORADA para criar gráficos
def create_advanced_charts(df):
    """Cria gráficos avançados e interativos - VERSÃO CORRIGIDA"""
    charts = {}
    
    try:
        st.info("🎨 Gerando visualizações avançadas...")
        progress_bar = st.progress(0)
        
        # 1. Gráfico de Barras 3D - Vendas por Região
        if 'vendas' in df.columns and 'regiao' in df.columns:
            progress_bar.progress(15)
            vendas_regiao = df.groupby('regiao').agg({
                'vendas': 'sum',
                'lucro': 'sum',
                'quantidade': 'sum'
            }).reset_index()
            
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
                textposition='outside',
                marker_line_color='white',
                marker_line_width=2
            )
            
            fig1.update_layout(
                height=500,
                title_x=0.5,
                title_font_size=20,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                coloraxis_colorbar=dict(title="Lucro (R$)")
            )
            
            charts['vendas_regiao'] = fig1
            st.success("✅ Gráfico 1/8 criado")
        
        # 2. Gráfico de Pizza Interativo - Distribuição por Categoria
        if 'categoria' in df.columns and 'vendas' in df.columns:
            progress_bar.progress(30)
            categoria_vendas = df.groupby('categoria')['vendas'].sum().reset_index()
            
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
                hovertemplate='<b>%{label}</b><br>Vendas: R$ %{value:,.0f}<br>Percentual: %{percent}<extra></extra>',
                pull=[0.1 if i == 0 else 0 for i in range(len(categoria_vendas))]
            )
            
            fig2.update_layout(
                height=500,
                title_x=0.5,
                title_font_size=20,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12)
            )
            
            charts['distribuicao_categoria'] = fig2
            st.success("✅ Gráfico 2/8 criado")
        
        # 3. Gráfico de Linha Múltipla - Tendência Temporal
        if 'vendas' in df.columns and 'mes' in df.columns:
            progress_bar.progress(45)
            meses_ordem = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
            
            vendas_mes = df.groupby('mes').agg({
                'vendas': 'sum',
                'lucro': 'sum',
                'quantidade': 'sum'
            }).reindex(meses_ordem, fill_value=0).reset_index()
            
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
                font=dict(size=12),
                legend=dict(x=0.02, y=0.98)
            )
            
            charts['tendencia_temporal'] = fig3
            st.success("✅ Gráfico 3/8 criado")
        
        # 4. Scatter Plot Avançado - Vendas vs Satisfação
        if 'vendas' in df.columns and 'satisfacao' in df.columns:
            progress_bar.progress(60)
            
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
                marker=dict(line=dict(width=1, color='white')),
                hovertemplate='<b>%{hovertext}</b><br>Satisfação: %{x}<br>Vendas: R$ %{y:,.0f}<br>Região: %{marker.color}<extra></extra>'
            )
            
            fig4.update_layout(
                height=500,
                title_x=0.5,
                title_font_size=20,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                xaxis=dict(title='Satisfação (1-5)', gridcolor='lightgray'),
                yaxis=dict(title='Vendas (R$)', gridcolor='lightgray')
            )
            
            charts['vendas_satisfacao'] = fig4
            st.success("✅ Gráfico 4/8 criado")
        
        # 5. Histograma Avançado - Distribuição de Vendas
        if 'vendas' in df.columns:
            progress_bar.progress(75)
            
            fig5 = px.histogram(
                df,
                x='vendas',
                nbins=25,
                title='📊 Distribuição de Vendas',
                color_discrete_sequence=['#4facfe'],
                marginal='box'
            )
            
            fig5.update_traces(
                marker=dict(line=dict(width=1, color='white')),
                hovertemplate='<b>Faixa de Vendas</b><br>R$ %{x:,.0f}<br>Quantidade: %{y}<extra></extra>'
            )
            
            fig5.update_layout(
                height=500,
                title_x=0.5,
                title_font_size=20,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                xaxis=dict(title='Vendas (R$)', gridcolor='lightgray'),
                yaxis=dict(title='Frequência', gridcolor='lightgray')
            )
            
            charts['distribuicao_vendas'] = fig5
            st.success("✅ Gráfico 5/8 criado")
        
        # 6. Box Plot Comparativo - Vendas por Produto
        if 'vendas' in df.columns and 'produto' in df.columns:
            progress_bar.progress(85)
            
            # Pegar apenas top 8 produtos para melhor visualização
            top_produtos = df.groupby('produto')['vendas'].sum().nlargest(8).index
            df_top = df[df['produto'].isin(top_produtos)]
            
            fig6 = px.box(
                df_top,
                x='produto',
                y='vendas',
                color='categoria',
                title='📦 Distribuição de Vendas por Produto (Top 8)',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            
            fig6.update_traces(
                hovertemplate='<b>%{x}</b><br>Vendas: R$ %{y:,.0f}<br>Categoria: %{marker.color}<extra></extra>'
            )
            
            fig6.update_layout(
                height=500,
                title_x=0.5,
                title_font_size=20,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                xaxis=dict(title='Produto', tickangle=45),
                yaxis=dict(title='Vendas (R$)', gridcolor='lightgray')
            )
            
            charts['vendas_produto'] = fig6
            st.success("✅ Gráfico 6/8 criado")
        
        # 7. Heatmap de Correlação
        if len(df.select_dtypes(include=[np.number]).columns) >= 3:
            progress_bar.progress(95)
            
            numeric_cols = ['vendas', 'lucro', 'margem', 'satisfacao', 'quantidade', 'desconto']
            available_cols = [col for col in numeric_cols if col in df.columns]
            
            if len(available_cols) >= 3:
                corr_matrix = df[available_cols].corr()
                
                fig7 = px.imshow(
                    corr_matrix,
                    title='🔥 Matriz de Correlação',
                    color_continuous_scale='RdBu',
                    aspect='auto',
                    text_auto=True
                )
                
                fig7.update_layout(
                    height=500,
                    title_x=0.5,
                    title_font_size=20,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12)
                )
                
                charts['correlacao'] = fig7
                st.success("✅ Gráfico 7/8 criado")
        
        # 8. Gráfico de Funil - Top Vendedores
        if 'vendedor' in df.columns and 'vendas' in df.columns:
            progress_bar.progress(100)
            
            top_vendedores = df.groupby('vendedor')['vendas'].sum().nlargest(10).reset_index()
            
            fig8 = go.Figure(go.Funnel(
                y=top_vendedores['vendedor'],
                x=top_vendedores['vendas'],
                textinfo="value+percent initial",
                hovertemplate='<b>%{y}</b><br>Vendas: R$ %{x:,.0f}<extra></extra>',
                marker=dict(
                    color=px.colors.sequential.Viridis,
                    line=dict(width=2, color='white')
                )
            ))
            
            fig8.update_layout(
                title='🏆 Top 10 Vendedores',
                height=500,
                title_x=0.5,
                title_font_size=20,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12)
            )
            
            charts['top_vendedores'] = fig8
            st.success("✅ Gráfico 8/8 criado")
        
        progress_bar.progress(100)
        time.sleep(0.5)
        progress_bar.empty()
        
        st.success(f"🎉 {len(charts)} gráficos criados com sucesso!")
        return charts
        
    except Exception as e:
        st.error(f"❌ Erro ao criar gráficos: {str(e)}")
        st.error(f"Detalhes: {type(e).__name__}")
        return {}

# Função para análise com Gemini AI MELHORADA
def analyze_with_gemini(df, custom_question=None):
    """Analisa dados com Gemini AI - Versão Melhorada"""
    gemini_status, status_msg = configure_gemini()
    
    if not gemini_status:
        return f"❌ Erro na configuração: {status_msg}"
    
    try:
        # Preparar estatísticas avançadas
        stats = {
            'total_records': len(df),
            'total_vendas': df['vendas'].sum() if 'vendas' in df.columns else 0,
            'total_lucro': df['lucro'].sum() if 'lucro' in df.columns else 0,
            'margem_media': df['margem'].mean() if 'margem' in df.columns else 0,
            'satisfacao_media': df['satisfacao'].mean() if 'satisfacao' in df.columns else 0,
            'top_regiao': df['regiao'].value_counts().index[0] if 'regiao' in df.columns else 'N/A',
            'top_produto': df['produto'].value_counts().index[0] if 'produto' in df.columns else 'N/A',
            'top_categoria': df['categoria'].value_counts().index[0] if 'categoria' in df.columns else 'N/A'
        }
        
        sample_data = df.head(3).to_dict('records')
        
        if custom_question:
            prompt = f"""
            🤖 ANALISTA DE DADOS ESPECIALISTA

            PERGUNTA ESPECÍFICA: {custom_question}
            
            📊 CONTEXTO DOS DADOS:
            • Total de registros: {stats['total_records']:,}
            • Vendas totais: R$ {stats['total_vendas']:,.0f}
            • Lucro total: R$ {stats['total_lucro']:,.0f}
            • Margem média: {stats['margem_media']:.1f}%
            • Satisfação média: {stats['satisfacao_media']:.1f}/5
            • Top região: {stats['top_regiao']}
            • Top produto: {stats['top_produto']}
            • Top categoria: {stats['top_categoria']}
            
            📋 AMOSTRA DOS DADOS:
            {json.dumps(sample_data, indent=2, ensure_ascii=False)}
            
            🎯 INSTRUÇÕES:
            • Responda em português brasileiro
            • Seja específico e use dados reais
            • Forneça insights acionáveis
            • Use emojis para destacar pontos importantes
            • Máximo 400 palavras
            """
        else:
            prompt = f"""
            🤖 CONSULTOR DE NEGÓCIOS ESPECIALISTA EM DADOS

            📊 ANÁLISE COMPLETA DO DATASET DE VENDAS
            
            📈 MÉTRICAS PRINCIPAIS:
            • Total de registros: {stats['total_records']:,}
            • Vendas totais: R$ {stats['total_vendas']:,.0f}
            • Lucro total: R$ {stats['total_lucro']:,.0f}
            • Margem média: {stats['margem_media']:.1f}%
            • Satisfação média: {stats['satisfacao_media']:.1f}/5
            • Região líder: {stats['top_regiao']}
            • Produto líder: {stats['top_produto']}
            • Categoria líder: {stats['top_categoria']}
            
            📋 AMOSTRA REPRESENTATIVA:
            {json.dumps(sample_data, indent=2, ensure_ascii=False)}
            
            🎯 FORNEÇA UMA ANÁLISE ESTRUTURADA:
            
            1. 📊 VISÃO GERAL DO NEGÓCIO
            • Performance geral das vendas
            • Principais características do dataset
            
            2. 🔍 INSIGHTS ESTRATÉGICOS (Top 3)
            • Descobertas mais importantes
            • Padrões identificados nos dados
            
            3. ⚠️ PONTOS DE ATENÇÃO
            • Problemas ou riscos identificados
            • Áreas que precisam de melhoria
            
            4. 🚀 RECOMENDAÇÕES PRÁTICAS (Top 3)
            • Ações específicas para melhorar resultados
            • Estratégias baseadas nos dados
            
            5. 📈 PRÓXIMOS PASSOS
            • Sugestões para análises futuras
            • KPIs para monitorar
            
            Use emojis, seja específico com números reais e forneça insights acionáveis.
            Máximo 600 palavras.
            """
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        return response.text
        
    except Exception as e:
        return f"❌ Erro na análise com IA: {str(e)}\n\n💡 Dica: Verifique sua chave API e conexão com a internet."

# Sidebar Ultra Melhorada
with st.sidebar:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 1.5rem; border-radius: 15px; text-align: center; margin-bottom: 1rem;">
        <h2 style="margin: 0;">🎛️ Painel de Controle</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Central de Comandos</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Status da IA com design melhorado
    st.markdown("### 🤖 Status da IA")
    gemini_status, status_msg = configure_gemini()
    
    if gemini_status:
        st.markdown(f"""
        <div class="success-alert">
            <strong>{status_msg}</strong><br>
            <small>Google Gemini AI ativo</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="error-alert">
            <strong>{status_msg}</strong><br>
            <small>Configure GEMINI_API_KEY</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Upload de arquivo melhorado
    st.markdown("### 📁 Carregar Dados")
    uploaded_file = st.file_uploader(
        "Escolha um arquivo",
        type=['csv', 'xlsx', 'json'],
        help="📋 Formatos: CSV, Excel, JSON\n📏 Tamanho máximo: 200MB"
    )
    
    # Botão para dados de exemplo melhorado
    if st.button("🎲 Gerar Dados de Exemplo", type="primary", use_container_width=True):
        with st.spinner("🔄 Gerando dataset avançado..."):
            st.session_state.df = generate_sample_data()
            st.session_state.data_loaded = True
            st.session_state.charts_generated = False
            st.success("✅ Dataset carregado com sucesso!")
            time.sleep(1)
            st.rerun()
    
    st.divider()
    
    # Informações do dataset
    if st.session_state.data_loaded and st.session_state.df is not None:
        df = st.session_state.df
        
        st.markdown("### 📊 Informações do Dataset")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📋 Registros", f"{len(df):,}")
            st.metric("📊 Colunas", len(df.columns))
        
        with col2:
            if 'vendas' in df.columns:
                st.metric("💰 Vendas", f"R$ {df['vendas'].sum()/1000:.0f}K")
            if 'lucro' in df.columns:
                st.metric("📈 Lucro", f"R$ {df['lucro'].sum()/1000:.0f}K")
        
        # Tamanho do arquivo
        size_mb = df.memory_usage(deep=True).sum() / 1024**2
        st.info(f"💾 Tamanho: {size_mb:.2f} MB")
        
        # Qualidade dos dados
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        if missing_pct == 0:
            st.success("✅ Dados completos")
        else:
            st.warning(f"⚠️ {missing_pct:.1f}% dados ausentes")

# Processamento do arquivo melhorado
if uploaded_file is not None:
    try:
        with st.spinner("📤 Processando arquivo..."):
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith('.json'):
                df = pd.read_json(uploaded_file)
            
            st.session_state.df = df
            st.session_state.data_loaded = True
            st.session_state.charts_generated = False
            
            st.success(f"✅ Arquivo '{uploaded_file.name}' carregado com sucesso!")
            st.info(f"📊 {len(df)} registros e {len(df.columns)} colunas carregados")
            time.sleep(1)
            st.rerun()
            
    except Exception as e:
        st.error(f"❌ Erro ao carregar arquivo: {str(e)}")
        st.info("💡 Dica: Verifique se o arquivo não está corrompido e está no formato correto")

# Interface principal ULTRA MELHORADA
if st.session_state.data_loaded and st.session_state.df is not None:
    df = st.session_state.df
    
    # Tabs com ícones melhorados
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard Executivo", 
        "📈 Visualizações Avançadas", 
        "🤖 IA Insights Pro", 
        "🔍 Explorador de Dados",
        "📥 Centro de Exportação"
    ])
    
    with tab1:
        st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
        st.markdown("## 📊 Dashboard Executivo")
        
        # Métricas principais com design ultra melhorado
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📋 Total de Registros</div>
                <div class="metric-number">{len(df):,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📊 Colunas de Dados</div>
                <div class="metric-number">{len(df.columns)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if 'vendas' in df.columns:
                total_vendas = df['vendas'].sum()
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">💰 Vendas Totais</div>
                    <div class="metric-number">R$ {total_vendas/1000000:.1f}M</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col4:
            if 'lucro' in df.columns:
                total_lucro = df['lucro'].sum()
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">📈 Lucro Total</div>
                    <div class="metric-number">R$ {total_lucro/1000000:.1f}M</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # KPIs adicionais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'margem' in df.columns:
                margem_media = df['margem'].mean()
                st.metric("📊 Margem Média", f"{margem_media:.1f}%", 
                         delta=f"{margem_media-30:.1f}%" if margem_media > 30 else None)
        
        with col2:
            if 'satisfacao' in df.columns:
                satisfacao_media = df['satisfacao'].mean()
                st.metric("⭐ Satisfação Média", f"{satisfacao_media:.1f}/5",
                         delta=f"{satisfacao_media-4:.1f}" if satisfacao_media > 4 else None)
        
        with col3:
            if 'ticket_medio' in df.columns:
                ticket_medio = df['ticket_medio'].mean()
                st.metric("🎫 Ticket Médio", f"R$ {ticket_medio:,.0f}")
        
        with col4:
            if 'roi' in df.columns:
                roi_medio = df['roi'].mean()
                st.metric("📈 ROI Médio", f"{roi_medio:.1f}%")
        
        st.markdown("---")
        
        # Análise detalhada em colunas
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Estatísticas Numéricas")
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                stats_df = df[numeric_cols].describe().round(2)
                st.dataframe(stats_df, use_container_width=True)
            else:
                st.info("ℹ️ Nenhuma coluna numérica encontrada")
        
        with col2:
            st.markdown("### 🔍 Qualidade dos Dados")
            
            missing_values = df.isnull().sum().sum()
            duplicates = df.duplicated().sum()
            memory_usage = df.memory_usage(deep=True).sum() / 1024**2
            
            quality_data = {
                'Métrica': ['Valores Ausentes', 'Linhas Duplicadas', 'Tamanho (MB)', 'Completude (%)'],
                'Valor': [
                    missing_values,
                    duplicates,
                    f"{memory_usage:.2f}",
                    f"{((len(df) * len(df.columns) - missing_values) / (len(df) * len(df.columns)) * 100):.1f}"
                ],
                'Status': [
                    '✅' if missing_values == 0 else '⚠️',
                    '✅' if duplicates == 0 else '⚠️',
                    '✅' if memory_usage < 100 else '⚠️',
                    '✅' if missing_values == 0 else '⚠️'
                ]
            }
            
            quality_df = pd.DataFrame(quality_data)
            st.dataframe(quality_df, hide_index=True, use_container_width=True)
        
        # Top insights rápidos
        st.markdown("### 🎯 Insights Rápidos")
        
        insight_col1, insight_col2, insight_col3 = st.columns(3)
        
        with insight_col1:
            if 'regiao' in df.columns and 'vendas' in df.columns:
                top_regiao = df.groupby('regiao')['vendas'].sum().idxmax()
                top_regiao_valor = df.groupby('regiao')['vendas'].sum().max()
                st.info(f"🏆 **Região Líder**: {top_regiao}\n\nVendas: R$ {top_regiao_valor:,.0f}")
        
        with insight_col2:
            if 'produto' in df.columns and 'vendas' in df.columns:
                top_produto = df.groupby('produto')['vendas'].sum().idxmax()
                top_produto_valor = df.groupby('produto')['vendas'].sum().max()
                st.success(f"🥇 **Produto Top**: {top_produto}\n\nVendas: R$ {top_produto_valor:,.0f}")
        
        with insight_col3:
            if 'vendedor' in df.columns and 'vendas' in df.columns:
                top_vendedor = df.groupby('vendedor')['vendas'].sum().idxmax()
                top_vendedor_valor = df.groupby('vendedor')['vendas'].sum().max()
                st.warning(f"⭐ **Vendedor Destaque**: {top_vendedor}\n\nVendas: R$ {top_vendedor_valor:,.0f}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
        st.markdown("## 📈 Visualizações Avançadas")
        
        # Botão para gerar gráficos
        if not st.session_state.charts_generated:
            if st.button("🎨 Gerar Visualizações Avançadas", type="primary", use_container_width=True):
                charts = create_advanced_charts(df)
                st.session_state.charts = charts
                st.session_state.charts_generated = True
                st.rerun()
        else:
            charts = st.session_state.get('charts', {})
        
        if st.session_state.charts_generated and charts:
            st.success(f"🎉 {len(charts)} visualizações criadas com sucesso!")
            
            # Organizar gráficos em grid responsivo
            chart_keys = list(charts.keys())
            
            # Primeira linha - 2 gráficos
            if len(chart_keys) >= 2:
                col1, col2 = st.columns(2)
                with col1:
                    if 'vendas_regiao' in charts:
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        st.plotly_chart(charts['vendas_regiao'], use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    if 'distribuicao_categoria' in charts:
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        st.plotly_chart(charts['distribuicao_categoria'], use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
            
            # Segunda linha - 1 gráfico grande
            if 'tendencia_temporal' in charts:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(charts['tendencia_temporal'], use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Terceira linha - 2 gráficos
            col1, col2 = st.columns(2)
            with col1:
                if 'vendas_satisfacao' in charts:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.plotly_chart(charts['vendas_satisfacao'], use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                if 'distribuicao_vendas' in charts:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.plotly_chart(charts['distribuicao_vendas'], use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Quarta linha - 2 gráficos
            col1, col2 = st.columns(2)
            with col1:
                if 'vendas_produto' in charts:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.plotly_chart(charts['vendas_produto'], use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                if 'correlacao' in charts:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.plotly_chart(charts['correlacao'], use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Quinta linha - 1 gráfico
            if 'top_vendedores' in charts:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(charts['top_vendedores'], use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Botão para regenerar
            if st.button("🔄 Regenerar Visualizações", use_container_width=True):
                st.session_state.charts_generated = False
                st.rerun()
        
        else:
            st.info("🎨 Clique no botão acima para gerar visualizações interativas avançadas")
            
            # Preview dos tipos de gráficos
            st.markdown("### 📊 Tipos de Visualizações Disponíveis:")
            
            preview_col1, preview_col2, preview_col3, preview_col4 = st.columns(4)
            
            with preview_col1:
                st.markdown("""
                **📊 Gráfico de Barras**
                - Vendas por região
                - Comparação visual
                - Dados interativos
                """)
            
            with preview_col2:
                st.markdown("""
                **🥧 Gráfico de Pizza**
                - Distribuição por categoria
                - Percentuais visuais
                - Hover detalhado
                """)
            
            with preview_col3:
                st.markdown("""
                **📈 Gráfico de Linha**
                - Tendências temporais
                - Múltiplas séries
                - Análise de padrões
                """)
            
            with preview_col4:
                st.markdown("""
                **💫 Scatter Plot**
                - Correlações
                - Múltiplas dimensões
                - Insights visuais
                """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
        st.markdown("## 🤖 IA Insights Pro")
        
        if gemini_status:
            # Botões de ação melhorados
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🚀 Análise Completa", type="primary", use_container_width=True):
                    with st.spinner("🤖 Analisando dados com Gemini AI..."):
                        analysis = analyze_with_gemini(df)
                        st.session_state.ai_analysis = analysis
            
            with col2:
                if st.button("🔄 Testar Conexão IA", use_container_width=True):
                    with st.spinner("🧪 Testando conexão..."):
                        test_result = analyze_with_gemini(df, "Responda apenas: 'IA funcionando perfeitamente!'")
                        if "funcionando" in test_result.lower():
                            st.success("✅ IA conectada e funcionando!")
                        else:
                            st.error("❌ Problema na conexão com IA")
            
            with col3:
                if st.button("⚡ Insights Rápidos", use_container_width=True):
                    with st.spinner("⚡ Gerando insights rápidos..."):
                        quick_analysis = analyze_with_gemini(df, "Dê 3 insights rápidos e práticos sobre estes dados")
                        st.session_state.quick_insights = quick_analysis
            
            st.markdown("---")
            
            # Pergunta customizada melhorada
            st.markdown("### 💬 Consultor IA Personalizado")
            
            # Sugestões de perguntas melhoradas
            suggestions = [
                "Quais são as 3 principais oportunidades de crescimento?",
                "Como posso aumentar a margem de lucro em 20%?",
                "Que produtos devo focar para maximizar vendas?",
                "Quais regiões têm maior potencial inexplorado?",
                "Como melhorar a satisfação do cliente?",
                "Que estratégias de pricing recomendam?",
                "Quais vendedores precisam de treinamento?",
                "Como otimizar o mix de produtos?",
                "Que tendências sazonais identificam?",
                "Como reduzir custos operacionais?"
            ]
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                selected_suggestion = st.selectbox(
                    "💡 Perguntas Sugeridas (ou digite a sua):",
                    [""] + suggestions,
                    help="Escolha uma pergunta ou digite sua própria pergunta personalizada"
                )
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                use_suggestion = st.button("📝 Usar Sugestão", use_container_width=True)
            
            custom_question = st.text_area(
                "🎯 Sua Pergunta Personalizada:",
                value=selected_suggestion if use_suggestion and selected_suggestion else "",
                placeholder="Ex: Como posso aumentar as vendas na região Norte em 30%?",
                height=100,
                help="Seja específico para obter insights mais precisos"
            )
            
            if st.button("🤖 Consultar IA Especialista", use_container_width=True) and custom_question:
                with st.spinner("🤖 Processando consulta especializada..."):
                    custom_analysis = analyze_with_gemini(df, custom_question)
                    st.session_state.custom_analysis = custom_analysis
                    st.session_state.last_question = custom_question
            
            st.markdown("---")
            
            # Exibir resultados com design melhorado
            if 'ai_analysis' in st.session_state:
                st.markdown("""
                <div class="insight-box">
                    <h3>🎯 Análise Completa do Gemini AI</h3>
                    <p>Insights estratégicos baseados em seus dados</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(st.session_state.ai_analysis)
                
                # Botão para nova análise
                if st.button("🔄 Nova Análise Completa"):
                    del st.session_state.ai_analysis
                    st.rerun()
            
            if 'quick_insights' in st.session_state:
                st.markdown("""
                <div class="insight-box">
                    <h3>⚡ Insights Rápidos</h3>
                    <p>Descobertas instantâneas dos seus dados</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(st.session_state.quick_insights)
            
            if 'custom_analysis' in st.session_state:
                st.markdown(f"""
                <div class="insight-box">
                    <h3>💬 Resposta Especializada</h3>
                    <p><strong>Pergunta:</strong> "{st.session_state.get('last_question', 'Pergunta personalizada')}"</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(st.session_state.custom_analysis)
                
                # Botão para nova pergunta
                if st.button("❓ Fazer Nova Pergunta"):
                    del st.session_state.custom_analysis
                    if 'last_question' in st.session_state:
                        del st.session_state.last_question
                    st.rerun()
        
        else:
            st.markdown("""
            <div class="error-alert">
                <h3>❌ IA Não Configurada</h3>
                <p>Configure a chave API do Google Gemini para usar esta funcionalidade</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🔧 Como Configurar:")
            st.code("""
# Método 1: Variável de ambiente
set GEMINI_API_KEY=sua_chave_aqui

# Método 2: Arquivo secrets
# Criar: .streamlit/secrets.toml
GEMINI_API_KEY = "sua_chave_aqui"
            """)
            
            st.info("🔑 Obtenha sua chave em: https://makersuite.google.com/app/apikey")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
        st.markdown("## 🔍 Explorador de Dados Avançado")
        
        # Filtros avançados
        st.markdown("### 🎛️ Filtros Inteligentes")
        
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            # Filtro categórico
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            if categorical_cols:
                selected_col = st.selectbox("📊 Filtrar por coluna:", ['Todas'] + categorical_cols)
                if selected_col != 'Todas':
                    unique_values = df[selected_col].unique()
                    selected_values = st.multiselect(
                        f"🎯 Valores de {selected_col}:", 
                        unique_values, 
                        default=unique_values[:5] if len(unique_values) > 5 else unique_values
                    )
                    df_filtered = df[df[selected_col].isin(selected_values)] if selected_values else df
                else:
                    df_filtered = df
            else:
                df_filtered = df
        
    with filter_col2:
        # Filtro numérico
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            numeric_col = st.selectbox("🔢 Filtro numérico:", ['Nenhum'] + numeric_cols)
            if numeric_col != 'Nenhum':
                min_val = float(df[numeric_col].min())
                max_val = float(df[numeric_col].max())
                range_vals = st.slider(
                    f"📏 Range de {numeric_col}:",
                    min_val, max_val, (min_val, max_val),
                    help=f"Valores entre {min_val:,.0f} e {max_val:,.0f}"
                )
                df_filtered = df_filtered[
                    (df_filtered[numeric_col] >= range_vals[0]) & 
                    (df_filtered[numeric_col] <= range_vals[1])
                ]
        
        with filter_col3:
            # Configurações de exibição
            n_rows = st.slider("📋 Linhas para exibir:", 5, min(100, len(df_filtered)), 20)
            show_stats = st.checkbox("📊 Mostrar estatísticas", True)
            show_charts = st.checkbox("📈 Gráficos rápidos", False)
        
        # Estatísticas dos dados filtrados
        if show_stats and len(df_filtered) > 0:
            st.markdown("### 📊 Estatísticas dos Dados Filtrados")
            
            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
            
            with stat_col1:
                st.metric("📋 Registros Filtrados", f"{len(df_filtered):,}")
            
            with stat_col2:
                if 'vendas' in df_filtered.columns:
                    total_vendas_filtered = df_filtered['vendas'].sum()
                    st.metric("💰 Vendas Filtradas", f"R$ {total_vendas_filtered/1000:.0f}K")
            
            with stat_col3:
                if 'lucro' in df_filtered.columns:
                    total_lucro_filtered = df_filtered['lucro'].sum()
                    st.metric("📈 Lucro Filtrado", f"R$ {total_lucro_filtered/1000:.0f}K")
            
            with stat_col4:
                filtro_pct = (len(df_filtered) / len(df)) * 100
                st.metric("🎯 % dos Dados", f"{filtro_pct:.1f}%")
        
        # Gráficos rápidos dos dados filtrados
        if show_charts and len(df_filtered) > 0:
            st.markdown("### 📈 Visualização Rápida dos Dados Filtrados")
            
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                if 'vendas' in df_filtered.columns and len(df_filtered) > 1:
                    fig_quick = px.histogram(
                        df_filtered, 
                        x='vendas', 
                        title='Distribuição de Vendas (Filtrado)',
                        color_discrete_sequence=['#667eea']
                    )
                    fig_quick.update_layout(height=300)
                    st.plotly_chart(fig_quick, use_container_width=True)
            
            with chart_col2:
                if 'regiao' in df_filtered.columns and 'vendas' in df_filtered.columns:
                    vendas_regiao_filtered = df_filtered.groupby('regiao')['vendas'].sum().reset_index()
                    fig_quick2 = px.bar(
                        vendas_regiao_filtered,
                        x='regiao',
                        y='vendas',
                        title='Vendas por Região (Filtrado)',
                        color_discrete_sequence=['#f093fb']
                    )
                    fig_quick2.update_layout(height=300)
                    st.plotly_chart(fig_quick2, use_container_width=True)
        
        # Tabela de dados melhorada
        st.markdown(f"### 📊 Dados Filtrados ({len(df_filtered):,} de {len(df):,} registros)")
        
        # Busca textual avançada
        search_col1, search_col2 = st.columns([3, 1])
        
        with search_col1:
            search_term = st.text_input(
                "🔎 Busca Textual Global:",
                placeholder="Digite qualquer termo para buscar em todas as colunas...",
                help="Busca em todas as colunas de texto"
            )
        
        with search_col2:
            st.markdown("<br>", unsafe_allow_html=True)
            case_sensitive = st.checkbox("🔤 Case Sensitive")
        
        # Aplicar busca se houver termo
        if search_term:
            mask = df_filtered.astype(str).apply(
                lambda x: x.str.contains(search_term, case=case_sensitive, na=False)
            ).any(axis=1)
            df_display = df_filtered[mask]
            st.info(f"🔍 Encontrados {len(df_display)} registros com '{search_term}'")
        else:
            df_display = df_filtered
        
        # Exibir tabela com formatação melhorada
        if len(df_display) > 0:
            st.dataframe(
                df_display.head(n_rows),
                use_container_width=True,
                height=400
            )
            
            # Informações adicionais
            if len(df_display) > n_rows:
                st.info(f"ℹ️ Mostrando {n_rows} de {len(df_display)} registros. Ajuste o slider para ver mais.")
        else:
            st.warning("⚠️ Nenhum registro encontrado com os filtros aplicados")
        
        # Análise rápida dos dados filtrados
        if len(df_display) > 0:
            st.markdown("### 🎯 Análise Rápida")
            
            analysis_col1, analysis_col2 = st.columns(2)
            
            with analysis_col1:
                st.markdown("**📊 Resumo Estatístico:**")
                numeric_cols_display = df_display.select_dtypes(include=[np.number]).columns
                if len(numeric_cols_display) > 0:
                    summary_stats = df_display[numeric_cols_display].describe().round(2)
                    st.dataframe(summary_stats.T[['mean', 'std', 'min', 'max']], use_container_width=True)
            
            with analysis_col2:
                st.markdown("**📋 Informações Categóricas:**")
                categorical_cols_display = df_display.select_dtypes(include=['object']).columns
                if len(categorical_cols_display) > 0:
                    for col in categorical_cols_display[:3]:  # Mostrar apenas 3 primeiras
                        unique_count = df_display[col].nunique()
                        most_common = df_display[col].mode().iloc[0] if len(df_display[col].mode()) > 0 else "N/A"
                        st.write(f"**{col}:** {unique_count} valores únicos, mais comum: {most_common}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab5:
        st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
        st.markdown("## 📥 Centro de Exportação")
        
        # Opções de exportação melhoradas
        export_col1, export_col2 = st.columns(2)
        
        with export_col1:
            st.markdown("### 📊 Exportar Dados Processados")
            
            # Preparar dados para download
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Seletor de dados para exportar
            export_option = st.radio(
                "📋 Dados para exportar:",
                ["Todos os dados", "Dados filtrados", "Apenas dados numéricos", "Resumo estatístico"]
            )
            
            if export_option == "Todos os dados":
                export_df = df
            elif export_option == "Dados filtrados" and 'df_filtered' in locals():
                export_df = df_filtered
            elif export_option == "Apenas dados numéricos":
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                export_df = df[numeric_cols]
            else:  # Resumo estatístico
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                export_df = df[numeric_cols].describe()
            
            st.info(f"📊 Preparando {len(export_df)} registros para exportação")
            
            # Botões de download melhorados
            col1, col2, col3 = st.columns(3)
            
            with col1:
                csv_data = export_df.to_csv(index=False)
                st.download_button(
                    label="📄 Download CSV",
                    data=csv_data,
                    file_name=f"datainsight_dados_{timestamp}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    help="Formato universal, compatível com Excel e outras ferramentas"
                )
            
            with col2:
                # Excel com múltiplas abas
                from io import BytesIO
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    export_df.to_excel(writer, sheet_name='Dados', index=False)
                    
                    # Adicionar aba com estatísticas se houver dados numéricos
                    numeric_cols = export_df.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 0:
                        export_df[numeric_cols].describe().to_excel(writer, sheet_name='Estatísticas')
                    
                    # Adicionar aba com análise da IA se existir
                    if 'ai_analysis' in st.session_state:
                        analysis_df = pd.DataFrame({
                            'Análise_IA': [st.session_state.ai_analysis]
                        })
                        analysis_df.to_excel(writer, sheet_name='Análise_IA', index=False)
                
                st.download_button(
                    label="📊 Download Excel",
                    data=buffer.getvalue(),
                    file_name=f"datainsight_relatorio_{timestamp}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    help="Relatório completo com múltiplas abas"
                )
            
            with col3:
                json_data = export_df.to_json(orient='records', indent=2)
                st.download_button(
                    label="📋 Download JSON",
                    data=json_data,
                    file_name=f"datainsight_dados_{timestamp}.json",
                    mime="application/json",
                    use_container_width=True,
                    help="Formato para APIs e desenvolvimento"
                )
        
        with export_col2:
            st.markdown("### 📈 Relatórios Especializados")
            
            # Relatório executivo
            if st.button("📊 Gerar Relatório Executivo", use_container_width=True):
                executive_report = f"""
RELATÓRIO EXECUTIVO - DATAINSIGHT AI PRO
========================================
Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Dataset: {len(df)} registros, {len(df.columns)} colunas

RESUMO EXECUTIVO:
================
• Total de Registros: {len(df):,}
• Total de Colunas: {len(df.columns)}
"""
                
                if 'vendas' in df.columns:
                    total_vendas = df['vendas'].sum()
                    executive_report += f"• Vendas Totais: R$ {total_vendas:,.2f}\n"
                
                if 'lucro' in df.columns:
                    total_lucro = df['lucro'].sum()
                    margem_total = (total_lucro / total_vendas * 100) if 'vendas' in df.columns else 0
                    executive_report += f"• Lucro Total: R$ {total_lucro:,.2f}\n"
                    executive_report += f"• Margem Total: {margem_total:.1f}%\n"
                
                if 'satisfacao' in df.columns:
                    satisfacao_media = df['satisfacao'].mean()
                    executive_report += f"• Satisfação Média: {satisfacao_media:.1f}/5\n"
                
                executive_report += f"""

TOP PERFORMERS:
==============
"""
                
                if 'regiao' in df.columns and 'vendas' in df.columns:
                    top_regiao = df.groupby('regiao')['vendas'].sum().idxmax()
                    top_regiao_valor = df.groupby('regiao')['vendas'].sum().max()
                    executive_report += f"• Região Líder: {top_regiao} (R$ {top_regiao_valor:,.0f})\n"
                
                if 'produto' in df.columns and 'vendas' in df.columns:
                    top_produto = df.groupby('produto')['vendas'].sum().idxmax()
                    top_produto_valor = df.groupby('produto')['vendas'].sum().max()
                    executive_report += f"• Produto Top: {top_produto} (R$ {top_produto_valor:,.0f})\n"
                
                if 'ai_analysis' in st.session_state:
                    executive_report += f"""

ANÁLISE DA IA:
=============
{st.session_state.ai_analysis}
"""
                
                executive_report += f"""

ESTATÍSTICAS DETALHADAS:
=======================
{df.describe().to_string()}

---
Relatório gerado automaticamente pelo DataInsight AI Pro
"""
                
                st.download_button(
                    label="📄 Download Relatório Executivo",
                    data=executive_report,
                    file_name=f"relatorio_executivo_{timestamp}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            # Relatório técnico
            if st.button("🔧 Gerar Relatório Técnico", use_container_width=True):
                technical_report = f"""
RELATÓRIO TÉCNICO - DATAINSIGHT AI PRO
======================================
Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

INFORMAÇÕES DO DATASET:
======================
• Nome: Dataset de Análise
• Registros: {len(df):,}
• Colunas: {len(df.columns)}
• Tamanho em Memória: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB
• Tipos de Dados: {dict(df.dtypes.value_counts())}

QUALIDADE DOS DADOS:
===================
• Valores Ausentes: {df.isnull().sum().sum()}
• Linhas Duplicadas: {df.duplicated().sum()}
• Completude: {((len(df) * len(df.columns) - df.isnull().sum().sum()) / (len(df) * len(df.columns)) * 100):.1f}%

ANÁLISE POR COLUNA:
==================
"""
                
                for col in df.columns:
                    technical_report += f"\n{col}:\n"
                    technical_report += f"  - Tipo: {df[col].dtype}\n"
                    technical_report += f"  - Valores únicos: {df[col].nunique()}\n"
                    technical_report += f"  - Valores ausentes: {df[col].isnull().sum()}\n"
                    
                    if df[col].dtype in ['int64', 'float64']:
                        technical_report += f"  - Mín: {df[col].min()}\n"
                        technical_report += f"  - Máx: {df[col].max()}\n"
                        technical_report += f"  - Média: {df[col].mean():.2f}\n"
                        technical_report += f"  - Desvio Padrão: {df[col].std():.2f}\n"
                
                technical_report += f"""

CORRELAÇÕES (COLUNAS NUMÉRICAS):
===============================
{df.select_dtypes(include=[np.number]).corr().to_string()}

---
Relatório técnico gerado pelo DataInsight AI Pro
"""
                
                st.download_button(
                    label="🔧 Download Relatório Técnico",
                    data=technical_report,
                    file_name=f"relatorio_tecnico_{timestamp}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            # Configurações de exportação
            st.markdown("### ⚙️ Configurações de Exportação")
            
            include_index = st.checkbox("📋 Incluir índice nos arquivos")
            date_format = st.selectbox("📅 Formato de data:", ["ISO (YYYY-MM-DD)", "BR (DD/MM/YYYY)", "US (MM/DD/YYYY)"])
            decimal_separator = st.selectbox("🔢 Separador decimal:", ["Ponto (.)", "Vírgula (,)"])
            
            st.info("⚙️ Configurações aplicadas aos próximos downloads")
        
        # Estatísticas de exportação
        st.markdown("---")
        st.markdown("### 📊 Resumo dos Dados para Exportação")
        
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
        
        with summary_col1:
            st.metric("📋 Total de Registros", f"{len(df):,}")
        
        with summary_col2:
            st.metric("📊 Total de Colunas", len(df.columns))
        
        with summary_col3:
            numeric_count = len(df.select_dtypes(include=[np.number]).columns)
            st.metric("🔢 Colunas Numéricas", numeric_count)
        
        with summary_col4:
            categorical_count = len(df.select_dtypes(include=['object']).columns)
            st.metric("📝 Colunas Categóricas", categorical_count)
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Tela inicial ULTRA MELHORADA
    st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
    
    # Hero section melhorada
    st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;" class="pulse">🚀</div>
        <h2 style="color: #667eea; margin-bottom: 2rem;">Bem-vindo ao DataInsight AI Pro!</h2>
        <p style="font-size: 1.2rem; color: #666; max-width: 800px; margin: 0 auto 2rem auto;">
            A plataforma mais avançada para análise de dados com inteligência artificial. 
            Transforme seus dados em insights poderosos com visualizações interativas e análise de IA de última geração.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid de funcionalidades melhorado
    st.markdown("### 🌟 Funcionalidades Principais")
    
    feature_col1, feature_col2, feature_col3 = st.columns(3)
    
    with feature_col1:
        st.markdown("""
        <div class="status-card">
            <h3>📊 Análise Avançada</h3>
            <ul>
                <li>✅ Estatísticas automáticas</li>
                <li>✅ Detecção de padrões</li>
                <li>✅ Qualidade dos dados</li>
                <li>✅ Correlações visuais</li>
                <li>✅ KPIs inteligentes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col2:
        st.markdown("""
        <div class="status-card">
            <h3>📈 Visualizações Pro</h3>
            <ul>
                <li>✅ 8 tipos de gráficos</li>
                <li>✅ Interatividade total</li>
                <li>✅ Design responsivo</li>
                <li>✅ Exportação HD</li>
                <li>✅ Animações suaves</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col3:
        st.markdown("""
        <div class="status-card">
            <h3>🤖 IA Avançada</h3>
            <ul>
                <li>✅ Google Gemini AI</li>
                <li>✅ Consultas personalizadas</li>
                <li>✅ Insights estratégicos</li>
                <li>✅ Recomendações práticas</li>
                <li>✅ Análise em tempo real</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Seção de como começar
    st.markdown("---")
    st.markdown("### 🎯 Como Começar")
    
    step_col1, step_col2, step_col3, step_col4 = st.columns(4)
    
    with step_col1:
        st.markdown("""
        **1️⃣ Carregue Dados**
        - 📁 Upload CSV/Excel/JSON
        - 🎲 Use dados de exemplo
        - 📏 Até 200MB suportado
        """)
    
    with step_col2:
        st.markdown("""
        **2️⃣ Explore Dashboard**
        - 📊 Métricas automáticas
        - 🔍 Qualidade dos dados
        - 📈 KPIs principais
        """)
    
    with step_col3:
        st.markdown("""
        **3️⃣ Visualize**
        - 🎨 Gráficos interativos
        - 📊 Múltiplas perspectivas
        - 💫 Correlações visuais
        """)
    
    with step_col4:
        st.markdown("""
        **4️⃣ Use IA**
        - 🤖 Configure Gemini API
        - 💬 Faça perguntas
        - 🎯 Obtenha insights
        """)
    
    # Botão de ação principal
    st.markdown("---")
    
    action_col1, action_col2, action_col3 = st.columns([1, 2, 1])
    with action_col2:
        if st.button("🎲 Começar com Dados de Exemplo", type="primary", use_container_width=True):
            with st.spinner("🔄 Gerando dataset avançado..."):
                st.session_state.df = generate_sample_data()
                st.session_state.data_loaded = True
                st.session_state.charts_generated = False
                st.success("✅ Dataset carregado! Explore as funcionalidades.")
                time.sleep(1)
                st.rerun()
        
        st.markdown("<div style='text-align: center; margin: 1rem 0;'><strong>ou</strong></div>", unsafe_allow_html=True)
        st.info("📁 Use a barra lateral para carregar seus próprios dados")
    
    # Seção de demonstração
    st.markdown("---")
    st.markdown("### 🎬 Demonstração")
    
    demo_col1, demo_col2 = st.columns(2)
    
    with demo_col1:
        st.markdown("""
        **📊 Exemplo de Análise:**
        - Dataset com 300 registros de vendas
        - 15+ colunas de dados
        - Múltiplas categorias e regiões
        - Dados correlacionados realistas
        """)
    
    with demo_col2:
        st.markdown("""
        **🎯 Insights Disponíveis:**
        - Performance por região
        - Análise de produtos
        - Satisfação do cliente
        - Tendências temporais
        """)
    
    # Footer informativo
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; margin: 2rem 0;">
        <h4>🚀 DataInsight AI Pro - Versão 2.0</h4>
        <p>Desenvolvido com Streamlit, Plotly, Pandas e Google Gemini AI</p>
        <p><strong>Recursos:</strong> Análise Avançada • Visualizações Interativas • IA Integrada • Exportação Completa</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
