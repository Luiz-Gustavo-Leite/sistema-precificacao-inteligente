# relatorio.py
import sqlite3
from pathlib import Path
import pandas as pd
from datetime import datetime

DB_FILE = Path(__file__).resolve().parent / "dados.db"
RELATORIO_DIR = Path(__file__).resolve().parent / "relatorios"
RELATORIO_DIR.mkdir(exist_ok=True)

def gerar_relatorio():
    """Gera um relatório Excel com os dados da tabela solicitacoes"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 🔧 Correção: usar os nomes reais das colunas da tabela 'solicitacoes'
    cursor.execute("SELECT canal, nome, preco, timestamp FROM solicitacoes ORDER BY timestamp DESC")
    dados = cursor.fetchall()
    conn.close()

    if not dados:
        raise Exception("Nenhum dado encontrado para gerar o relatório.")

    # Cria DataFrame com nomes de colunas compatíveis
    df = pd.DataFrame(dados, columns=["Canal", "Nome", "Preço (R$)", "Data/Hora"])

    # Define nome do arquivo com data/hora atual
    agora = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho_arquivo = RELATORIO_DIR / f"relatorio_{agora}.xlsx"

    # Salva o relatório em Excel
    df.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo