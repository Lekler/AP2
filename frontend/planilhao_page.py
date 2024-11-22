from backend.routers import menu_planilhao
from backend.views import pegar_df_preco_corrigido, pegar_df_preco_diversos
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date, datetime


def app():
    st.title("PLANILHAO")
    data_base = st.date_input("Digite a data base:")
    df = menu_planilhao(data_base)
    if df is not None:
        st.dataframe(df)

        # Adicionar gráficos de preços corrigidos e diversos
        if not df.empty:
            tickers = df['ticker'].tolist()
            data_ini = st.date_input("Selecione a Data Inicial:")
            data_fim = st.date_input("Selecione a Data Final:")
            top_n = st.slider(
                "Selecione o número de ativos a serem visualizados:", 1, len(tickers), 10)

            if data_ini > data_fim:
                st.error("A data inicial não pode ser posterior à data final.")
                return

            if data_fim > datetime.now().date():
                st.error("A data final não pode ser posterior à data atual.")
                return

            if st.button("Gerar Grafico de Precos Corrigidos"):
                df_preco_corrigido = pegar_df_preco_corrigido(
                    data_ini, data_fim, tickers, top_n)
                if 'data' in df_preco_corrigido.columns:
                    df_preco_corrigido['fechamento'] = df_preco_corrigido['fechamento'].astype(
                        float)
                    df_grafico = df_preco_corrigido.groupby(
                        "data")["fechamento"].sum()
                    sns.lineplot(data=df_grafico)
                    st.pyplot(plt)
                else:
                    st.error(
                        "Erro: A coluna 'data' não está presente no DataFrame.")

            if st.button("Gerar Grafico de Precos Diversos"):
                df_preco_diversos = pegar_df_preco_diversos(
                    data_ini, data_fim, tickers, top_n)
                if 'data' in df_preco_diversos.columns:
                    df_preco_diversos['fechamento'] = df_preco_diversos['fechamento'].astype(
                        float)
                    df_grafico = df_preco_diversos.groupby(
                        "data")["fechamento"].sum()
                    sns.lineplot(data=df_grafico)
                    st.pyplot(plt)
                else:
                    st.error(
                        "Erro: A coluna 'data' não está presente no DataFrame.")
    else:
        st.write("Sem Dados no Planilhão para a data selecionada.")
