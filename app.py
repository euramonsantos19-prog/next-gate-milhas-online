import streamlit as st
import pandas as pd

st.set_page_config(page_title="Next Gate Milhas Online")

st.title("Next Gate Milhas Online")

uploaded_file = st.file_uploader("Upload da base de milhas", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    # Padronizar nomes das colunas
    df.columns = df.columns.str.strip().str.lower()

    # Converter valores tipo 24K -> 24000
    def converter_k(valor):
        if isinstance(valor, str):
            valor = valor.replace("K", "000").replace("k", "000")
        return valor

    if "média por cpf" in df.columns:
        df["média por cpf"] = df["média por cpf"].apply(converter_k)

    # Converter colunas numéricas
    df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce")
    df["cpf"] = pd.to_numeric(df["cpf"], errors="coerce")
    df["média por cpf"] = pd.to_numeric(df["média por cpf"], errors="coerce")
    df["custo do milheiro"] = pd.to_numeric(df["custo do milheiro"], errors="coerce")

    st.subheader("Base carregada")
    st.dataframe(df)

    # Filtros
    programa = st.selectbox(
        "Programa",
        df["programa"].dropna().unique()
    )

    milhas_desejadas = st.number_input(
        "Milhas desejadas",
        min_value=0,
        step=1000
    )

    cpf_necessario = st.number_input(
        "CPF necessários",
        min_value=0
    )

    media_limite = st.number_input(
        "Média por CPF",
        min_value=0
    )

    if st.button("Buscar contas disponíveis"):

        resultado = df[
            (df["programa"] == programa) &
            (df["quantidade"] >= milhas_desejadas) &
            (df["cpf"] >= cpf_necessario) &
            (df["média por cpf"] <= media_limite)
        ]

        # ordenar pelo menor custo
        resultado = resultado.sort_values(by="custo do milheiro")

        if resultado.empty:

            st.warning("Nenhuma conta encontrada com saldo suficiente.")

        else:

            st.subheader("Contas disponíveis")
            st.dataframe(resultado)

            melhor = resultado.iloc[0]

            custo_total = (
                milhas_desejadas / 1000
            ) * melhor["custo do milheiro"]

            st.success(
                f"Custo estimado total: R$ {round(custo_total,2)}"
            )
