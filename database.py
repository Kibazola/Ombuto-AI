
import sqlite3


def conectar():
    """Estabelece a ligação à base de dados do Ombuto AI."""
    conexao = sqlite3.connect("ombuto.db")
    return conexao


def criar_tabela():
    """Cria a tabela de despesas caso ainda não exista."""
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS despesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            categoria TEXT NOT NULL,
            valor REAL NOT NULL,
            data DATE NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


if __name__ == "__main__":
    criar_tabela()
    print("Base de dados do Ombuto AI preparada com sucesso!")