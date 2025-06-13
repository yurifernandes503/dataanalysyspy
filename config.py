"""
Configurações do DataInsight AI
"""

import os
import streamlit as st

# Configurações da aplicação
APP_CONFIG = {
    'title': 'DataInsight AI',
    'icon': '🤖',
    'layout': 'wide',
    'sidebar_state': 'expanded'
}

# Configurações do Gemini AI
GEMINI_CONFIG = {
    'model': 'gemini-1.5-flash',
    'temperature': 0.7,
    'top_p': 0.8,
    'top_k': 40,
    'max_output_tokens': 1024
}

# Configurações de visualização
PLOT_CONFIG = {
    'height': 500,
    'color_palette': ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'],
    'template': 'plotly_white'
}

# Configurações de dados
DATA_CONFIG = {
    'max_file_size': 200,  # MB
    'supported_formats': ['csv', 'xlsx', 'json'],
    'sample_size': 500
}

def get_gemini_api_key():
    """Obtém a chave API do Gemini"""
    return st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

def validate_dataframe(df):
    """Valida se o DataFrame está em formato adequado"""
    if df is None or df.empty:
        return False, "DataFrame vazio"
    
    if len(df) > 100000:
        return False, "Dataset muito grande (máximo 100.000 registros)"
    
    return True, "DataFrame válido"
