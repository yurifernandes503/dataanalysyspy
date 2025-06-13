"""
Script para gerar dados de exemplo para o DataInsight AI
Execute: python dados_exemplo.py
"""

import pandas as pd
import numpy as np
from datetime import datetime

def criar_dados_vendas():
    """Cria dataset de vendas para demonstração"""
    np.random.seed(42)
    
    # Configurações
    n_records = 500
    
    # Listas de dados
    vendedores = [
        'João Silva', 'Maria Santos', 'Pedro Costa', 'Ana Lima', 
        'Carlos Rocha', 'Lucia Ferreira', 'Roberto Alves', 'Fernanda Dias',
        'Marcos Oliveira', 'Patricia Souza', 'Ricardo Mendes', 'Juliana Castro'
    ]
    
    produtos = [
        'Smartphone Pro', 'Laptop Gamer', 'Tablet Ultra', 'Smartwatch Fit',
        'Fones Bluetooth', 'Camera Digital', 'Console Game', 'Monitor 4K',
        'Teclado Mecânico', 'Mouse Gamer', 'SSD 1TB', 'Placa de Vídeo'
    ]
    
    regioes = ['Norte', 'Sul', 'Leste', 'Oeste', 'Centro']
    
    meses = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ]
    
    categorias = ['Eletrônicos', 'Informática', 'Games', 'Acessórios', 'Mobile']
    
    canais = ['Online', 'Loja Física', 'Marketplace', 'Telefone', 'App Mobile']
    
    # Gerar dados
    data = []
    
    for i in range(n_records):
        # Categoria influencia preço
        categoria = np.random.choice(categorias)
        
        if categoria == 'Eletrônicos':
            vendas_base = np.random.normal(25000, 8000)
        elif categoria == 'Informática':
            vendas_base = np.random.normal(35000, 12000)
        elif categoria == 'Games':
            vendas_base = np.random.normal(15000, 5000)
        elif categoria == 'Mobile':
            vendas_base = np.random.normal(20000, 7000)
        else:  # Acessórios
            vendas_base = np.random.normal(8000, 3000)
        
        vendas = max(1000, int(vendas_base))
        custo = int(vendas * np.random.uniform(0.4, 0.7))
        lucro = vendas - custo
        margem = (lucro / vendas) * 100
        
        # Satisfação correlacionada com margem
        if margem > 40:
            satisfacao = np.random.choice([4, 5], p=[0.3, 0.7])
        elif margem > 25:
            satisfacao = np.random.choice([3, 4, 5], p=[0.2, 0.5, 0.3])
        else:
            satisfacao = np.random.choice([1, 2, 3], p=[0.3, 0.4, 0.3])
        
        # Tempo de entrega baseado no canal
        canal = np.random.choice(canais)
        if canal == 'Online':
            tempo_entrega = np.random.randint(1, 7)
        elif canal == 'Loja Física':
            tempo_entrega = 0  # Retirada imediata
        else:
            tempo_entrega = np.random.randint(2, 15)
        
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
            'canal': canal,
            'satisfacao': satisfacao,
            'quantidade': np.random.randint(1, 50),
            'desconto': round(np.random.uniform(0, 0.30), 3),
            'tempo_entrega': tempo_entrega,
            'data_venda': np.random.choice(pd.date_range('2024-01-01', '2024-12-31', freq='D')).strftime('%Y-%m-%d')
        })
    
    # Criar DataFrame
    df = pd.DataFrame(data)
    
    # Salvar arquivo
    filename = f'dados_vendas_exemplo_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    df.to_csv(filename, index=False)
    
    print(f"✅ Arquivo '{filename}' criado com {len(df)} registros!")
    print(f"\n📊 Resumo dos dados:")
    print(f"- Total de vendas: R$ {df['vendas'].sum():,.0f}")
    print(f"- Total de lucro: R$ {df['lucro'].sum():,.0f}")
    print(f"- Margem média: {df['margem'].mean():.1f}%")
    print(f"- Satisfação média: {df['satisfacao'].mean():.1f}")
    
    print(f"\n📈 Por categoria:")
    print(df.groupby('categoria')['vendas'].sum().sort_values(ascending=False))
    
    print(f"\n🌍 Por região:")
    print(df.groupby('regiao')['vendas'].sum().sort_values(ascending=False))
    
    return df

if __name__ == "__main__":
    print("🚀 Gerando dados de exemplo para DataInsight AI...")
    df = criar_dados_vendas()
    print("\n✅ Dados gerados com sucesso!")
    print("📁 Use este arquivo CSV na aplicação Streamlit")
