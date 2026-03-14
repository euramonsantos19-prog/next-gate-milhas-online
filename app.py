import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Next Gate Milhas",
    layout="wide"
)

# =========================
# HEADER
# =========================

st.markdown(
"""
<style>

.main-title{
font-size:28px;
font-weight:600;
}

.metric-card{
background-color:#f5f5f5;
padding:15px;
border-radius:10px;
}

</style>
""",
unsafe_allow_html=True
)

st.markdown('<div class="main-title">Next Gate Milhas Online</div>', unsafe_allow_html=True)

# =========================
# CARREGAR BASE
# =========================

@st.cache_data
def carregar_base():

    df = pd.read_excel("base.xlsx")

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace("á","a")
        .str.replace("é","e")
        .str.replace("í","i")
        .str.replace("ó","o")
        .str.replace("ú","u")
    )

    def tratar_media(valor):

        if isinstance(valor,str):

            valor = valor.strip()

            if valor in ["∞","inf","infinito"]:
                return 0

            valor = valor.replace("K","000").replace("k","000")

        return valor

    df["media por cpf"] = df["media por cpf"].apply(tratar_media)

    df["quantidade"] = pd.to_numeric(df["quantidade"],errors="coerce")
    df["cpf"] = pd.to_numeric(df["cpf"],errors="coerce")
    df["media por cpf"] = pd.to_numeric(df["media por cpf"],errors="coerce")
    df["custo do milheiro"] = pd.to_numeric(df["custo do milheiro"],errors="coerce")

    return df

df = carregar_base()

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.header("Filtros")

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

# =========================
# CALCULO MÉDIA
# =========================

media_por_cpf = milhas_desejadas / cpf_necessarios if cpf_necessarios > 0 else 0

st.write(
    "Média por CPF calculada automaticamente:",
    f"{int(media_por_cpf):,}".replace(",",".")
)

# =========================
# BUSCA AUTOMATICA
# =========================

if milhas_desejadas > 0:

    resultado = df[
        (df["programa"] == programa) &
        (df["quantidade"] >= milhas_desejadas) &
        (df["cpf"] >= cpf_necessarios) &
        (
            (df["media por cpf"] == 0) |
            (df["media por cpf"] <= media_por_cpf)
        )
    ].copy()

    if resultado.empty:

        st.warning("Nenhuma conta encontrada.")

    else:

        resultado["diferenca"] = resultado["quantidade"] - milhas_desejadas
        resultado = resultado.sort_values(by=["diferenca","custo do milheiro"])

        melhor = resultado.iloc[0]

        st.markdown("## ⭐ Melhor oferta encontrada")

        c1,c2,c3,c4,c5,c6 = st.columns(6)

        c1.metric("ID",melhor["id"])
        c2.metric("Fornecedor",melhor["fornecedor"])
        c3.metric("Titular",melhor["titular"])
        c4.metric("Quantidade",f"{int(melhor['quantidade']):,}".replace(",","."))
        c5.metric("CPF",int(melhor["cpf"]))

        c6.metric(
            "Custo Milheiro",
            f"R$ {melhor['custo do milheiro']:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X",".")
        )

        custo_total = (milhas_desejadas/1000)*melhor["custo do milheiro"]

        custo_total = (
            f"R$ {custo_total:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X",".")
        )

        st.success(f"Custo estimado total: {custo_total}")

        # =========================
        # TOP 3
        # =========================

        st.markdown("### 🏆 Top 3 melhores contas")

        top3 = resultado.head(3)

        for i,(_,row) in enumerate(top3.iterrows(),start=1):

            quantidade = f"{int(row['quantidade']):,}".replace(",", ".")

            custo = (
                f"R$ {row['custo do milheiro']:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X",".")
            )

            st.write(
                f"{i}️⃣ ID {row['id']} | "
                f"{row['fornecedor']} | "
                f"{row['titular']} | "
                f"{quantidade} milhas | "
                f"CPF {int(row['cpf'])} | "
                f"{custo}"
            )

        # =========================
        # TABELA
        # =========================

        st.markdown("## Contas disponíveis")

        def formatar_milhar(valor):
            return f"{int(valor):,}".replace(",", ".")

        resultado["quantidade"] = resultado["quantidade"].apply(formatar_milhar)

        resultado["media por cpf"] = resultado["media por cpf"].apply(
            lambda x:"∞" if x==0 else f"{int(x*1000):,}".replace(",",".")
        )

        resultado["custo do milheiro"] = resultado["custo do milheiro"].apply(
            lambda x:f"R$ {x:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X",".")
        )

        st.dataframe(
            resultado.drop(columns=["diferenca"]),
            use_container_width=True
        )
