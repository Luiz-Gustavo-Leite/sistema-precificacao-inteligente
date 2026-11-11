import sqlite3
from flask import request, jsonify, session
from werkzeug.security import check_password_hash
from pathlib import Path

DB_FILE = Path(__file__).resolve().parent / "dados.db"


def login_user():

    data = request.get_json() or {}

    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, password, perfil FROM usuarios WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 401

    if not check_password_hash(user[2], password):
        return jsonify({"error": "Senha inválida"}), 401

    session["user_id"] = user[0]
    session["perfil"] = user[3]

    return jsonify({
        "success": True,
        "perfil": user[3]
    })

from functools import wraps
from flask import redirect


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'user_id' not in session:
            return redirect('/')

        return f(*args, **kwargs)

    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if session.get('perfil') != 'admin':
            return jsonify({
                'error': 'Acesso negado'
            }), 403

        return f(*args, **kwargs)

    return decorated_function