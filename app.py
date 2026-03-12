import streamlit as st
import pandas as pd

st.title("Next Gate Milhas Online")

st.write("Sistema de busca de ofertas de milhas")

uploaded_file = st.file_uploader("Upload da base de milhas (Excel)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.write("Base carregada:")
    st.dataframe(df)

    programa = st.selectbox("Programa", df["Programa"].unique())

    quantidade = st.number_input("Quantidade de milhas desejadas", min_value=0)

    cpf = st.number_input("CPF necessários", min_value=0)

    media = st.number_input("Média por CPF", min_value=0)

    if st.button("Buscar ofertas"):

        resultado = df[
            (df["Programa"] == programa) &
            (df["Quantidade"] >= quantidade) &
            (df["CPF"] >= cpf) &
            (df["Média por CPF"] <= media)
        ]

        st.write("Ofertas encontradas:")

        st.dataframe(resultado)
