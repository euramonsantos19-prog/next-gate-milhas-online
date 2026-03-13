import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Next Gate Milhas Online",
    layout="wide"
)

st.title("Next Gate Milhas Online")

# carregar base fixa
df = pd.read_excel("base.xlsx")

# padronizar colunas
df.columns = df.columns.str.strip().str.lower()

# converter valores tipo 24K
def converter_k(valor):
    if isinstance(valor, str):
        valor = valor.replace("K", "000").replace("k", "000")
    return valor

if "média por cpf" in df.columns:
    df["média por cpf"] = df["média por cpf"].apply(converter_k)

# converter colunas numéricas
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

# cálculo automático da média
media_por_cpf = milhas_desejadas / cpf_necessarios

st.write(
    "Média por CPF calculada automaticamente:",
    f"{int(media_por_cpf):,}".replace(",", ".")
)

if st.button("Buscar contas disponíveis"):

    resultado = df[
        (df["programa"] == programa) &
        (df["quantidade"] >= milhas_desejadas) &
        (df["cpf"] >= cpf_necessarios) &
        (df["média por cpf"] <= media_por_cpf)
    ]

    resultado = resultado.sort_values(
        by="custo do milheiro"
    )

    if resultado.empty:

        st.warning("Nenhuma conta encontrada com saldo suficiente.")

    else:

        st.subheader("Contas disponíveis")

        # formatar milhar
        def formatar_milhar(valor):
            return f"{int(valor):,}".replace(",", ".")

        resultado["quantidade"] = resultado["quantidade"].apply(formatar_milhar)

        # média por cpf multiplicada por 1000
        resultado["média por cpf"] = resultado["média por cpf"].apply(
            lambda x: f"{int(x*1000):,}".replace(",", ".")
        )

        # custo milheiro formatado
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

        melhor = resultado.iloc[0]

        custo_milheiro = float(
            melhor["custo do milheiro"]
            .replace("R$ ", "")
            .replace(".", "")
            .replace(",", ".")
        )

        custo_total = (milhas_desejadas / 1000) * custo_milheiro

        custo_total_formatado = (
            f"R$ {custo_total:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        st.success(
            f"Custo estimado total: {custo_total_formatado}"
        )
