import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import date
from backend.apis import obter_preco_acoes
from backend.views import calcular_rendimento


def app():
    st.title("Gráficos de Ações")

    # Entrada de dados
    st.write("Digite os tickers das ações que deseja analisar, separados por vírgula. Exemplo: PETR4, VALE3, BBAS3")
    tickers = st.text_input("Digite os tickers (separados por vírgula):")
    data_inicio = st.date_input("Data de Início:")
    data_fim = st.date_input("Data de Fim:")

    if st.button("Gerar Gráficos"):
        if data_inicio > data_fim:
            st.error("A data inicial não pode ser posterior à data final.")
            return

        tickers_list = tickers.split(",")
        df_precos = pd.DataFrame()

        # Obter dados de preços
        for ticker in tickers_list:
            dados_preco = obter_preco_acoes(
                ticker.strip(), data_inicio, data_fim)
            if dados_preco:
                df_ticker = calcular_rendimento(dados_preco)
                df_precos[ticker.strip()] = df_ticker['fechamento']
            else:
                st.error(f"Erro ao obter dados de preços para {ticker}")

        # Converter os índices para datetime e os valores para float
        if not df_precos.empty:
            df_precos.index = pd.to_datetime(df_precos.index)
            df_precos = df_precos.astype(float)

            # Gráfico de preços
            st.subheader("Histórico de Preços")
            fig, ax = plt.subplots(figsize=(14, 7))
            for column in df_precos.columns:
                ax.plot(df_precos.index, df_precos[column], label=column)
            ax.set_title("Histórico de Preços")
            ax.set_xlabel("Data")
            ax.set_ylabel("Preço")
            ax.legend()
            st.pyplot(fig)

            # Gráfico de retornos
            st.subheader("Retornos Diários")
            retornos = df_precos.pct_change().dropna()
            fig, ax = plt.subplots(figsize=(14, 7))
            for column in retornos.columns:
                ax.plot(retornos.index, retornos[column], label=column)
            ax.set_title("Retornos Diários")
            ax.set_xlabel("Data")
            ax.set_ylabel("Retorno")
            ax.legend()
            st.pyplot(fig)

            # Matriz de correlação
            if not retornos.empty:
                st.subheader("Matriz de Correlação")
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(retornos.corr(), annot=True,
                            cmap='coolwarm', ax=ax)
                ax.set_title("Matriz de Correlação")
                st.pyplot(fig)
            else:
                st.write(
                    "Não há dados suficientes para gerar a matriz de correlação.")
        else:
            st.write("Não há dados suficientes para gerar os gráficos.")
