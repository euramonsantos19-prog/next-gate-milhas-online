import streamlit as st
import pandas as pd

st.title("Next Gate Milhas Online")

uploaded_file = st.file_uploader("Upload da base de milhas (Excel)", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    # Padroniza nomes das colunas
    df.columns = df.columns.str.strip().str.lower()

    # Converter colunas numéricas
    df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce")
    df["cpf"] = pd.to_numeric(df["cpf"], errors="coerce")
    df["média por cpf"] = pd.to_numeric(df["média por cpf"], errors="coerce")

    st.write("Colunas detectadas:")
    st.write(df.columns)

    programa = st.selectbox("Programa", df["programa"].dropna().unique())

    quantidade = st.number_input("Quantidade de milhas desejadas", min_value=0)

    cpf = st.number_input("CPF necessários", min_value=0)

    media = st.number_input("Média por CPF", min_value=0)

    if st.button("Buscar ofertas"):

        resultado = df[
            (df["programa"] == programa) &
            (df["quantidade"] >= quantidade) &
            (df["cpf"] >= cpf) &
            (df["média por cpf"] <= media)
        ]

        st.write("Ofertas encontradas:")
        st.dataframe(resultado)
