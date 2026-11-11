"""Cria o primeiro administrador do Sistema de Precificação Inteligente.

Execute a partir da raiz do repositorio com:
    python backend/create_admin.py
"""

from getpass import getpass
import sqlite3

from database import init_db, init_users_table, create_user, list_users


def main():
    init_db()
    init_users_table()

    if any(user["perfil"] == "admin" for user in list_users()):
        print("Ja existe um administrador cadastrado. Por seguranca, nenhum usuario foi criado.")
        return

    username = input("Nome de usuario para o administrador: ").strip()
    if not username:
        print("O nome de usuario nao pode ficar vazio.")
        return

    password = getpass("Senha (minimo de 12 caracteres): ")
    confirmation = getpass("Confirme a senha: ")

    if len(password) < 12:
        print("A senha precisa ter pelo menos 12 caracteres.")
        return
    if password != confirmation:
        print("As senhas nao conferem.")
        return

    try:
        create_user(username, password, "admin")
    except sqlite3.IntegrityError:
        print("Esse nome de usuario ja existe. Escolha outro.")
        return

    print("Administrador criado com sucesso. Guarde a senha em local seguro.")


if __name__ == "__main__":
    main()
