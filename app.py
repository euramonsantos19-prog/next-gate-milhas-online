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

if milhas_restantes > 0:

    st.warning("Não foi possível atingir a quantidade desejada.")

else:

    st.subheader("Melhor combinação encontrada")
    st.data
