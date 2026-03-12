import streamlit as st
import pandas as pd

st.title("Next Gate Milhas Online")

uploaded_file = st.file_uploader("Upload da base de milhas", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    # padronizar colunas
    df.columns = df.columns.str.strip().str.lower()

    # converter valores tipo 24K
    def converter_k(valor):
        if isinstance(valor, str):
            valor = valor.replace("K","000").replace("k","000")
        return valor

    df["média por cpf"] = df["média por cpf"].apply(converter_k)

    df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce")
    df["cpf"] = pd.to_numeric(df["cpf"], errors="coerce")
    df["média por cpf"] = pd.to_numeric(df["média por cpf"], errors="coerce")
    df["custo do milheiro"] = pd.to_numeric(df["custo do milheiro"], errors="coerce")

    programa = st.selectbox("Programa", df["programa"].dropna().unique())

    milhas_desejadas = st.number_input("Milhas desejadas", min_value=0)

    cpf_necessario = st.number_input("CPF necessários", min_value=0)

    media_limite = st.number_input("Média por CPF", min_value=0)

    if st.button("Encontrar melhor combinação"):

        ofertas = df[
            (df["programa"] == programa) &
            (df["cpf"] >= cpf_necessario) &
            (df["média por cpf"] <= media_limite)
        ]

        ofertas = ofertas.sort_values(by="custo do milheiro")

        milhas_restantes = milhas_desejadas
        combinacao = []

        for _, row in ofertas.iterrows():

            if milhas_restantes <= 0:
                break

            milhas_disponiveis = row["quantidade"]
            milhas_usadas = min(milhas_disponiveis, milhas_restantes)

            nova_linha = row.copy()
            nova_linha["milhas_usadas"] = milhas_usadas

            combinacao.append(nova_linha)

            milhas_restantes -= milhas_usadas

        resultado = pd.DataFrame(combinacao)

        if resultado.empty:
            st.warning("Nenhuma oferta encontrada.")

        elif milhas_restantes > 0:
            st.warning("Não foi possível atingir a quantidade desejada.")
            st.subheader("Combinação parcial encontrada")
            st.dataframe(resultado)

        else:
            st.subheader("Melhor combinação encontrada")
            st.dataframe(resultado)

            custo_total = (resultado["milhas_usadas"].sum() / 1000) * resultado.iloc[0]["custo do milheiro"]

            st.success(f"Custo estimado total: R$ {round(custo_total,2)}")
