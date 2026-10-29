
import sqlite3
from datetime import date

from database import criar_tabela, conectar


def registar_despesa():
    """Solicita os dados e guarda uma despesa na base de dados."""

    print("\n--- REGISTAR DESPESA ---")

    descricao = input("Descrição da despesa: ").strip()
    categoria = input("Categoria: ").strip()

    try:
        valor = float(input("Valor da despesa (R$): ").replace(",", "."))

        if valor <= 0:
            print("Erro: o valor deve ser superior a zero.")
            return

    except ValueError:
        print("Erro: introduz um valor numérico válido.")
        return

    data_despesa = input(
        f"Data (AAAA-MM-DD) ou Enter para hoje [{date.today()}]: "
    ).strip()

    if not data_despesa:
        data_despesa = date.today().isoformat()

    try:
        date.fromisoformat(data_despesa)
    except ValueError:
        print("Erro: a data deve estar no formato AAAA-MM-DD.")
        return

    if not descricao or not categoria:
        print("Erro: a descrição e a categoria são obrigatórias.")
        return

    conexao = conectar()

    conexao.execute(
        """
        INSERT INTO despesas (descricao, categoria, valor, data)
        VALUES (?, ?, ?, ?)
        """,
        (descricao, categoria, valor, data_despesa),
    )

    conexao.commit()
    conexao.close()

    print("\nDespesa registada com sucesso!")


def listar_despesas():
    """Apresenta todas as despesas registadas."""

    conexao = conectar()

    despesas = conexao.execute(
        """
        SELECT id, descricao, categoria, valor, data
        FROM despesas
        ORDER BY data DESC, id DESC
        """
    ).fetchall()

    conexao.close()

    print("\n--- HISTÓRICO DE DESPESAS ---")

    if not despesas:
        print("Ainda não existem despesas registadas.")
        return

    total = 0

    for despesa in despesas:
        identificador, descricao, categoria, valor, data_despesa = despesa
        total += valor

        print(
            f"ID: {identificador} | "
            f"Descrição: {descricao} | "
            f"Categoria: {categoria} | "
            f"Valor: R$ {valor:.2f} | "
            f"Data: {data_despesa}"
        )

    print(f"\nTotal das despesas: R$ {total:.2f}")


def menu():
    """Apresenta o menu principal do Ombuto AI."""

    criar_tabela()

    while True:
        print("\n==============================")
        print("        OMBUTO AI")
        print(" Gestão Inteligente de Despesas")
        print("==============================")
        print("1. Registar despesa")
        print("2. Consultar despesas")
        print("3. Sair")

        opcao = input("\nEscolhe uma opção: ").strip()

        if opcao == "1":
            registar_despesa()
        elif opcao == "2":

            
            listar_despesas()
        elif opcao == "3":
            print("Obrigado por utilizares o Ombuto AI!")
            break
        else:
            print("Opção inválida. Escolhe 1, 2 ou 3.")


if __name__ == "__main__":
    menu()