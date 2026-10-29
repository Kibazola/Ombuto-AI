import sqlite3
from datetime import date

import pandas as pd
import streamlit as st

from database import criar_tabela, conectar


# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Ombuto AI | Gestão Financeira",
    page_icon="🌱",
    layout="wide",
)

criar_tabela()


# ==========================================
# ESTILO VISUAL
# ==========================================

st.markdown(
    """
    <style>
        /* Fundo geral */
        .stApp {
            background-color: #F7F9F7;
        }

        /* Títulos */
        h1, h2, h3, h4 {
            color: #173D2B !important;
        }

        /* Textos gerais */
        .stApp,
        .stApp p,
        .stApp label,
        .stApp span,
        .stApp div[data-testid="stCaptionContainer"] {
            color: #26352C;
        }

        /* Indicadores financeiros */
        div[data-testid="stMetric"] {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #D5E3D8;
        }

        div[data-testid="stMetric"] label {
            color: #52665A !important;
        }

        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: #216E45 !important;
        }

        /* Campos de preenchimento */
        .stTextInput input,
        .stNumberInput input,
        .stDateInput input {
            color: #26352C !important;
            background-color: #FFFFFF !important;
        }

        /* Botões */
        div.stButton > button,
        div.stFormSubmitButton > button {
            background-color: #216E45;
            color: #FFFFFF !important;
            border-radius: 8px;
            border: none;
        }

        div.stButton > button:hover,
        div.stFormSubmitButton > button:hover {
            background-color: #174D30;
            color: #FFFFFF !important;
        }

        /* Cartões e separadores */
        hr {
            border-color: #D5E3D8;
        }
    </style>
     """,
    unsafe_allow_html=True,
)


# ==========================================
# FUNÇÕES DA BASE DE DADOS
# ==========================================

def obter_despesas():
    """Obtém as despesas guardadas na base de dados."""

    conexao = conectar()

    despesas = conexao.execute(
        """
        SELECT id, descricao, categoria, valor, data
        FROM despesas
        ORDER BY data DESC, id DESC
        """
    ).fetchall()

    conexao.close()

    return despesas


def guardar_despesa(descricao, categoria, valor, data_despesa):
    """Guarda uma nova despesa."""

    conexao = conectar()

    conexao.execute(
        """
        INSERT INTO despesas (descricao, categoria, valor, data)
        VALUES (?, ?, ?, ?)
        """,
        (descricao, categoria, valor, data_despesa.isoformat()),
    )

    conexao.commit()
    conexao.close()


# ==========================================
# CABEÇALHO
# ==========================================

st.title("🌱 Ombuto AI")
st.caption("Gestão inteligente de despesas | O teu dinheiro, sob controlo.")

st.divider()


# ==========================================
# CARREGAR OS DADOS
# ==========================================

despesas = obter_despesas()

colunas = ["ID", "Descrição", "Categoria", "Valor (R$)", "Data"]

df = pd.DataFrame(despesas, columns=colunas)

if not df.empty:
    df["Data"] = pd.to_datetime(df["Data"])
    df["Valor (R$)"] = pd.to_numeric(df["Valor (R$)"])


# ==========================================
# INDICADORES FINANCEIROS
# ==========================================

total_despesas = df["Valor (R$)"].sum() if not df.empty else 0
quantidade_despesas = len(df)

maior_despesa = (
    df["Valor (R$)"].max()
    if not df.empty
    else 0
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "💰 Total gasto",
    f"R$ {total_despesas:,.2f}",
)

col2.metric(
    "🧾 Despesas registadas",
    quantidade_despesas,
)

col3.metric(
    "📈 Maior despesa",
    f"R$ {maior_despesa:,.2f}",
)

st.divider()


# ==========================================
# REGISTAR DESPESAS
# ==========================================

st.subheader("📝 Registar nova despesa")

with st.form("formulario_despesa", clear_on_submit=True):

    descricao = st.text_input(
        "Descrição",
        placeholder="Ex.: Compra de supermercado",
    )

    categoria = st.selectbox(
        "Categoria",
        [
            "Alimentação",
            "Transporte",
            "Habitação",
            "Educação",
            "Saúde",
            "Lazer",
            "Tecnologia",
            "Outros",
        ],
    )

    col4, col5 = st.columns(2)

    with col4:
        valor = st.number_input(
            "Valor (R$)",
            min_value=0.0,
            value=0.0,
            step=1.0,
            format="%.2f",
        )

    with col5:
        data_despesa = st.date_input(
            "Data da despesa",
            value=date.today(),
        )

    enviar = st.form_submit_button("Guardar despesa")

    if enviar:

        if not descricao.strip():
            st.error("Introduz uma descrição para a despesa.")

        elif valor <= 0:
            st.error("O valor deve ser superior a zero.")

        else:
            guardar_despesa(
                descricao.strip(),
                categoria,
                valor,
                data_despesa,
            )

            st.success("Despesa registada com sucesso!")

            st.rerun()


st.divider()


# ==========================================
# GRÁFICO POR CATEGORIA
# ==========================================

st.subheader("📊 Análise de despesas por categoria")

if not df.empty:

    gastos_categoria = (
        df.groupby("Categoria")["Valor (R$)"]
        .sum()
        .sort_values(ascending=False)
    )

    col_grafico, col_resumo = st.columns([2, 1])

    with col_grafico:
        st.bar_chart(gastos_categoria)

    with col_resumo:
        st.markdown("#### Distribuição dos gastos")

        for categoria_nome, valor_categoria in gastos_categoria.items():

            percentagem = (
                valor_categoria / total_despesas * 100
                if total_despesas > 0
                else 0
            )

            st.write(f"**{categoria_nome}**")
            st.progress(float(percentagem / 100))
            st.caption(
                f"R$ {valor_categoria:,.2f} — {percentagem:.1f}%"
            )

else:
    st.info(
        "Ainda não existem despesas para analisar. "
        "Regista a tua primeira despesa para gerar os gráficos."
    )


st.divider()


# ==========================================
# HISTÓRICO DE DESPESAS
# ==========================================

st.subheader("📋 Histórico de despesas")

if not df.empty:

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Valor (R$)": st.column_config.NumberColumn(
                "Valor (R$)",
                format="R$ %.2f",
            ),
            "Data": st.column_config.DateColumn(
                "Data",
                format="DD/MM/YYYY",
            ),
        },
    )

    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="📥 Exportar despesas para CSV",
        data=csv,
        file_name="despesas_ombuto.csv",
        mime="text/csv",
    )

else:
    st.info("O histórico aparecerá aqui depois do primeiro registo.")


st.divider()

st.caption("Ombuto AI | Desenvolvido para tornar a gestão financeira mais simples.")