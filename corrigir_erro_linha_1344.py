"""
Script para corrigir o erro de sintaxe na linha 1344
"""

import os
import re

def corrigir_erro_sintaxe():
    """Corrige o erro de sintaxe na linha 1344 do app.py"""
    
    # Caminho do arquivo
    caminho_arquivo = "app.py"
    
    # Verificar se o arquivo existe
    if not os.path.exists(caminho_arquivo):
        print(f"❌ Arquivo {caminho_arquivo} não encontrado!")
        return False
    
    # Ler o arquivo
    with open(caminho_arquivo, 'r', encoding='utf-8') as file:
        linhas = file.readlines()
    
    # Verificar se tem linhas suficientes
    if len(linhas) < 1344:
        print(f"❌ O arquivo tem apenas {len(linhas)} linhas, não chega até a linha 1344!")
        return False
    
    # Obter a linha com erro
    linha_com_erro = linhas[1343]  # índice 1343 = linha 1344
    print(f"Linha com erro: {linha_com_erro.strip()}")
    
    # Verificar se a linha contém o padrão do erro
    if "help=f\"Valores entre {min_val:.0f} e {max_val:.0f}\"" in linha_com_erro:
        # Corrigir a linha - adicionar vírgula se estiver faltando
        if not linha_com_erro.strip().endswith(","):
            linhas[1343] = linha_com_erro.rstrip() + ",\n"
            print(f"✅ Linha corrigida: {linhas[1343].strip()}")
        else:
            print("⚠️ A linha já tem vírgula no final!")
    else:
        # Tentar corrigir outros problemas de sintaxe comuns
        # Verificar se há parênteses desbalanceados
        if linha_com_erro.count("(") != linha_com_erro.count(")"):
            print("⚠️ Parênteses desbalanceados na linha!")
            # Tentar corrigir
            if linha_com_erro.count("(") > linha_com_erro.count(")"):
                linhas[1343] = linha_com_erro.rstrip() + ")\n"
                print(f"✅ Linha corrigida: {linhas[1343].strip()}")
        else:
            print("⚠️ Não foi possível identificar o erro específico!")
            print("Sugestão: Verifique manualmente a sintaxe da linha 1344")
    
    # Salvar o arquivo corrigido
    with open(caminho_arquivo + ".corrigido", 'w', encoding='utf-8') as file:
        file.writelines(linhas)
    
    print(f"✅ Arquivo corrigido salvo como {caminho_arquivo}.corrigido")
    print("⚠️ Renomeie para app.py após verificar as alterações!")
    
    return True

if __name__ == "__main__":
    print("🔧 Corretor de Erro de Sintaxe - Linha 1344")
    print("=" * 50)
    
    corrigir_erro_sintaxe()
