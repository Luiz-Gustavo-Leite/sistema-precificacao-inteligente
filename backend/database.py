# database.py

from werkzeug.security import generate_password_hash
import sqlite3
from pathlib import Path
from typing import Dict, Any, List

DB_FILE = Path(__file__).resolve().parent / "dados.db"


# =========================================
# INICIALIZA BANCO
# =========================================

def init_db():

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # =========================================
    # TABELA PRINCIPAL
    # =========================================

    c.execute("""
    CREATE TABLE IF NOT EXISTS solicitacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        canal INTEGER NOT NULL,
        nome TEXT NOT NULL,
        preco REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # =========================================
    # HISTÓRICO
    # =========================================

    c.execute("""
    CREATE TABLE IF NOT EXISTS historico_precos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        canal INTEGER NOT NULL,
        nome TEXT NOT NULL,
        preco REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()


# =========================================
# INSERIR SOLICITAÇÃO
# =========================================

def insert_solicitacao(canal: int, nome: str, preco: float):

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # salva solicitação principal
    c.execute(
        "INSERT INTO solicitacoes (canal, nome, preco) VALUES (?, ?, ?)",
        (canal, nome, preco)
    )

    # salva histórico
    c.execute(
        "INSERT INTO historico_precos (canal, nome, preco) VALUES (?, ?, ?)",
        (canal, nome, preco)
    )

    conn.commit()
    conn.close()


# =========================================
# LISTAR HISTÓRICO
# =========================================

def list_recent(limit: int = 50) -> List[Dict[str, Any]]:

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""
        SELECT id, canal, nome, preco, timestamp
        FROM solicitacoes
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = c.fetchall()

    conn.close()

    return [
        {
            "id": r[0],
            "canal": r[1],
            "nome": r[2],
            "preco": r[3],
            "timestamp": r[4]
        }
        for r in rows
    ]


# =========================================
# TABELA DE USUÁRIOS
# =========================================

def init_users_table():

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        perfil TEXT
    )
    """)

    conn.commit()
    conn.close()


# ======================================
# CRIAR USUÁRIO
# ======================================

def create_user(username, password, perfil):

    conn = sqlite3.connect(DB_FILE)

    c = conn.cursor()

    hashed = generate_password_hash(password)

    c.execute(
        """
        INSERT INTO usuarios(username, password, perfil)
        VALUES (?, ?, ?)
        """,
        (username, hashed, perfil)
    )

    conn.commit()

    conn.close()


# ======================================
# LISTAR USUÁRIOS
# ======================================

def list_users():

    conn = sqlite3.connect(DB_FILE)

    c = conn.cursor()

    c.execute(
        """
        SELECT id, username, perfil
        FROM usuarios
        ORDER BY id DESC
        """
    )

    rows = c.fetchall()

    conn.close()

    return [
        {
            "id": r[0],
            "username": r[1],
            "perfil": r[2]
        }
        for r in rows
    ]


# ======================================
# EXCLUIR USUÁRIO
# ======================================

def delete_user(user_id):

    conn = sqlite3.connect(DB_FILE)

    c = conn.cursor()

    c.execute(
        "DELETE FROM usuarios WHERE id = ?",
        (user_id,)
    )

    conn.commit()

    conn.close()