import streamlit as st
import pandas as pd

st.title("Next Gate Milhas Online")

uploaded_file = st.file_uploader("Upload da base de milhas", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    # Padronizar nomes das colunas
    df.columns = df.columns.str.strip().str.lower()

    # Converter valores tipo 24K para número
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

    st
