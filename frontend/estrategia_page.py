import streamlit as st
from backend.routers import botao_gerar_estrategia
from backend.views import pegar_df_preco_corrigido, pegar_df_preco_diversos
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns

def app():
    st.title("Estrategia Page")

    # Explicações dos indicadores
    indicadores = {
        "roe": "ROE (Return on Equity) é uma medida de rentabilidade que calcula o retorno sobre o patrimônio líquido.",
        "roc": "ROC (Return on Capital) é uma medida de rentabilidade que calcula o retorno sobre o capital investido.",
        "roic": "ROIC (Return on Invested Capital) é uma medida de rentabilidade que calcula o retorno sobre o capital total investido.",
        "earning_yield": "Earning Yield é a relação entre o lucro por ação e o preço da ação, indicando o rendimento dos lucros.",
        "dividend_yield": "Dividend Yield é a relação entre o dividendo pago por ação e o preço da ação, indicando o rendimento dos dividendos.",
        "p_vp": "P/VP (Preço sobre Valor Patrimonial) é a relação entre o preço da ação e o valor patrimonial por ação, indicando se a ação está cara ou barata."
    }

    ind_rentabilidade = st.radio("Selecione o indicador de rentabilidade", ["roe", "roc", "roic"])
    st.write(indicadores[ind_rentabilidade])

    ind_desconto = st.radio("Selecione o indicador de desconto", ["earning_yield", "dividend_yield", "p_vp"])
    st.write(indicadores[ind_desconto])

    data_base = st.date_input("Selecione a Data Base:")
    qtde_acoes = st.text_input("Digite o numero de acoes da carteira:")

    if st.button("Gerar Estrategia"):
        df = botao_gerar_estrategia(data_base, ind_rentabilidade, ind_desconto, int(qtde_acoes))
        if df is not None:
            st.table(df)

            # Exibir gráfico de preços corrigidos
            data_ini = st.date_input("Selecione a Data Inicial:")
            data_fim = st.date_input("Selecione a Data Final:")
            top_n = st.slider("Selecione o número de ativos a serem visualizados:", 1, len(df), 10)
            carteira = df['ticker'].tolist()

            if data_ini > data_fim:
                st.error("A data inicial não pode ser posterior à data final.")
                return

            if st.button("Gerar Grafico de Precos Corrigidos"):
                df_preco_corrigido = pegar_df_preco_corrigido(data_ini, data_fim, carteira, top_n)
                df_grafico = df_preco_corrigido.groupby("data")["fechamento"].sum()
                sns.lineplot(data=df_grafico)
                st.pyplot(plt)

            if st.button("Gerar Grafico de Precos Diversos"):
                df_preco_diversos = pegar_df_preco_diversos(data_ini, data_fim, carteira, top_n)
                df_grafico = df_preco_diversos.groupby("data")["fechamento"].sum()
                sns.lineplot(data=df_grafico)
                st.pyplot(plt)
        else:
            st.write("Sem dados para a estratégia selecionada.")
