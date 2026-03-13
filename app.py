import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Next Gate Milhas Online",
    layout="wide"
)

st.title("Next Gate Milhas Online")

df = pd.read_excel("base.xlsx")

df.columns = df.columns.str.strip().str.lower()

def tratar_media(valor):

    if isinstance(valor, str):

        valor = valor.strip()

        if valor in ["∞", "inf", "infinito"]:
            return 0

        valor = valor.replace("K", "000").replace("k", "000")

    return valor

df["média por cpf"] = df["média por cpf"].apply(tratar_media)

df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce")
df["cpf"] = pd.to_numeric(df["cpf"], errors="coerce")
df["média por cpf"] = pd.to_numeric(df["média por cpf"], errors="coerce")
df["custo do milheiro"] = pd.to_numeric(df["custo do milheiro"], errors="coerce")

programa = st.selectbox(
    "Programa",
    df["programa"].dropna().unique()
)

milhas_desejadas = st.number_input(
    "Milhas desejadas",
    min_value=0,
    step=1000
)

cpf_necessarios = st.number_input(
    "CPF necessários",
    min_value=1
)

media_por_cpf = milhas_desejadas / cpf_necessarios

st.write(
    "Média por CPF calculada automaticamente:",
    f"{int(media_por_cpf):,}".replace(",", ".")
)

if st.button("Buscar contas disponíveis"):

    resultado = df[
        (df["programa"] == programa) &
        (df["quantidade"] >= milhas_desejadas) &
        (df["cpf"] <= cpf_necessarios) &
        (
            (df["média por cpf"] == 0) |
            (df["média por cpf"] <= media_por_cpf)
        )
    ]

    resultado = resultado.sort_values(
        by="custo do milheiro"
    )

    if resultado.empty:

        st.warning("Nenhuma conta encontrada com saldo suficiente.")

    else:

        melhor = resultado.iloc[0]

        st.markdown("## ⭐ Melhor oferta encontrada")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Fornecedor",
            melhor["fornecedor"]
        )

        col2.metric(
            "Quantidade",
            f"{int(melhor['quantidade']):,}".replace(",", ".")
        )

        col3.metric(
            "CPF",
            int(melhor["cpf"])
        )

        col4.metric(
            "Custo do milheiro",
            f"R$ {melhor['custo do milheiro']:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        custo_total = (milhas_desejadas / 1000) * melhor["custo do milheiro"]

        custo_total_formatado = (
            f"R$ {custo_total:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        st.success(
            f"Custo estimado total: {custo_total_formatado}"
        )

        st.markdown("## Outras contas disponíveis")

        def formatar_milhar(valor):
            return f"{int(valor):,}".replace(",", ".")

        resultado["quantidade"] = resultado["quantidade"].apply(formatar_milhar)

        resultado["média por cpf"] = resultado["média por cpf"].apply(
            lambda x: "∞" if x == 0 else f"{int(x*1000):,}".replace(",", ".")
        )

        resultado["custo do milheiro"] = resultado["custo do milheiro"].apply(
            lambda x: f"R$ {x:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        st.dataframe(
            resultado,
            use_container_width=True
        )
