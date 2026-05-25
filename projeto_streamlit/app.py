import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Dashboard Brasileirão",
    layout="wide"
)



df = pd.read_csv("dados/brasileirao.csv")

st.title("⚽ Dashboard Estatístico do Campeonato Brasileiro")
st.markdown("Análise simples e interativa utilizando Python e Streamlit")


st.sidebar.header("🔎 Filtros")


lista_times = df["time_casa"].unique()


time_escolhido = st.sidebar.selectbox(
    "Selecione um time",
    ["Todos"] + list(lista_times)
)


if time_escolhido != "Todos":
    df_filtrado = df[
        (df["time_casa"] == time_escolhido) |
        (df["time_fora"] == time_escolhido)
    ]
else:
    df_filtrado = df


total_gols = (
    df_filtrado["gols_casa"].sum() +
    df_filtrado["gols_fora"].sum()
)


media_gols = total_gols / len(df_filtrado)


total_partidas = len(df_filtrado)


total_cartoes = (
    df_filtrado["cartoes_amarelos"].sum() +
    df_filtrado["cartoes_vermelhos"].sum()
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("⚽ Total de Gols", total_gols)

with col2:
    st.metric("📊 Média de Gols", round(media_gols, 2))

with col3:
    st.metric("🏟️ Partidas", total_partidas)

with col4:
    st.metric("🟨 Cartões", total_cartoes)

st.divider()


st.subheader("📌 Insights do Campeonato")


gols_por_time = df.groupby("time_casa")["gols_casa"].sum()


time_mais_gols = gols_por_time.idxmax()
qtd_gols = gols_por_time.max()

st.success(
    f"O time com mais gols como mandante foi "
    f"{time_mais_gols} com {qtd_gols} gols."
)


st.subheader("📈 Gols por Time")

grafico_gols = (
    df.groupby("time_casa")["gols_casa"]
    .sum()
    .sort_values(ascending=False)
)

fig1, ax1 = plt.subplots(figsize=(10, 5))

ax1.bar(grafico_gols.index, grafico_gols.values)

ax1.set_title("Total de Gols por Time")
ax1.set_xlabel("Times")
ax1.set_ylabel("Gols")

plt.xticks(rotation=90)

st.pyplot(fig1)


st.subheader("📉 Média de Gols por Rodada")


df["total_gols"] = (
    df["gols_casa"] +
    df["gols_fora"]
)


media_rodada = (
    df.groupby("rodada")["total_gols"]
    .mean()
)

fig2, ax2 = plt.subplots(figsize=(10, 5))

ax2.plot(
    media_rodada.index,
    media_rodada.values
)

ax2.set_title("Média de Gols por Rodada")
ax2.set_xlabel("Rodada")
ax2.set_ylabel("Média de Gols")

st.pyplot(fig2)


st.subheader("🥧 Distribuição de Resultados")


vitorias_casa = len(
    df[df["gols_casa"] > df["gols_fora"]]
)

empates = len(
    df[df["gols_casa"] == df["gols_fora"]]
)

vitorias_fora = len(
    df[df["gols_casa"] < df["gols_fora"]]
)

labels = [
    "Vitória Casa",
    "Empates",
    "Vitória Fora"
]

valores = [
    vitorias_casa,
    empates,
    vitorias_fora
]

fig3, ax3 = plt.subplots(figsize=(6, 6))

ax3.pie(
    valores,
    labels=labels,
    autopct="%1.1f%%"
)

ax3.set_title("Distribuição dos Resultados")

st.pyplot(fig3)


st.subheader("📋 Tabela de Dados")

st.dataframe(df_filtrado)


st.subheader("📊 Estatísticas Automáticas")


st.write(df_filtrado.describe())


st.markdown("---")

st.caption(
    "Projeto desenvolvido para análise "
    "estatística do Campeonato Brasileiro."
)