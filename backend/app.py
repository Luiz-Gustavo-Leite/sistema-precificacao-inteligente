# app.py

from flask import Flask, send_from_directory, request, jsonify, redirect, url_for, send_file, session
from pathlib import Path
import os
from dotenv import load_dotenv
from flask_cors import CORS
from precificacao import parse_preco, format_preco, DEFAULT_ITENS
from database import (
    init_db,
    insert_solicitacao,
    list_recent,
    init_users_table,
    create_user,
    list_users,
    delete_user
)
from oled_display import OLEDController
from relatorio import gerar_relatorio
from auth import login_user, login_required, admin_required

# =========================================
# CONFIG PATHS
# =========================================

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

# Carrega as variaveis locais sem incluir segredos no codigo-fonte.
load_dotenv(BASE_DIR / ".env")

# =========================================
# INIT DATABASE
# =========================================

init_db()
init_users_table()

# =========================================
# OLED
# =========================================

oled = OLEDController()

# =========================================
# FLASK
# =========================================

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="/")

CORS(app)

app.secret_key = os.getenv("FLASK_SECRET_KEY")

if not app.secret_key:
    raise RuntimeError(
        "A variavel FLASK_SECRET_KEY nao foi definida. "
        "Crie um arquivo .env na raiz do projeto usando .env.example como modelo."
    )

# =========================================
# LOGIN PAGE
# =========================================

@app.route("/")
def home():

    return send_from_directory(FRONTEND_DIR, "login.html")


# =========================================
# SYSTEM PAGE
# =========================================

@app.route('/system')
@login_required
def system():

    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route('/display')
def display():
    return send_from_directory(FRONTEND_DIR, "display.html")


# =========================================
# STATIC FILES
# =========================================

@app.route("/<path:filename>")
def static_files(filename):

    return send_from_directory(str(FRONTEND_DIR), filename)


# =========================================
# UPDATE OLED
# =========================================

@app.route("/api/update", methods=["POST"])
def api_update():

    data = request.get_json() or {}

    try:

        canal = int(data.get("canal", 2))
        nome = str(data.get("nome", "")).strip()
        preco = float(data.get("preco", 0.0))

    except Exception as e:

        return jsonify({
            "error": "dados inválidos",
            "detail": str(e)
        }), 400

    insert_solicitacao(canal, nome, preco)

    try:

        preco_str = format_preco(preco)

        oled.render_item(
            canal,
            nome,
            preco_str,
            notice="Dados atualizados",
            notice_ms=900
        )

    except Exception as e:

        print(f"[WARN] falha render oled: {e}")

    return jsonify({
        "ok": True
    })


# =========================================
# ITEMS / HISTÓRICO
# =========================================

@app.route("/api/items", methods=["GET"])
def api_items():

    recent = list_recent(20)

    return jsonify({
        "defaults": DEFAULT_ITENS,
        "recent": recent
    })


# =========================================
# RELATÓRIO
# =========================================

@app.route("/api/relatorio", methods=["GET"])
@login_required
def api_relatorio():

    try:

        caminho = gerar_relatorio()

        return send_file(
            caminho,
            as_attachment=True
        )

    except Exception as e:

        import traceback

        traceback.print_exc()

        print(f"[ERRO RELATÓRIO] {e}")

        return jsonify({
            "error": str(e)
        }), 500


# =========================================
# LOGIN
# =========================================

@app.route('/api/login', methods=['POST'])
def login():

    return login_user()


# =========================================
# LOGOUT
# =========================================

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')

# ======================================
# LISTAR USUÁRIOS
# ======================================

@app.route('/api/users', methods=['GET'])
@login_required
@admin_required
def api_users():

    return jsonify(list_users())


# ======================================
# CRIAR USUÁRIO
# ======================================

@app.route('/api/users', methods=['POST'])
@login_required
@admin_required
def api_create_user():

    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    perfil = data.get('perfil')

    try:

        create_user(username, password, perfil)

        return jsonify({
            'success': True
        })

    except Exception as e:

        return jsonify({
            'error': str(e)
        }), 400


# ======================================
# EXCLUIR USUÁRIO
# ======================================

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@login_required
@admin_required
def api_delete_user(user_id):

    delete_user(user_id)

    return jsonify({
        'success': True
    })


# =========================================
# RUN SERVER
# =========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )