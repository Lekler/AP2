import streamlit as st
from backend.views import pegar_df_planilhao, gerar_estrategia, pegar_df_preco_corrigido, pegar_df_preco_diversos, calcular_rendimento, analisar_roe, analisar_magic_formula


def menu_planilhao(data_base):
    df = pegar_df_planilhao(data_base)
    return df


def botao_gerar_estrategia(data_base, ind_rentabilidade, ind_desconto, qtde_acoes):
    df = gerar_estrategia(data_base, ind_rentabilidade,
                          ind_desconto, qtde_acoes)
    return df


def gerar_grafico_precos_corrigidos(data_ini, data_fim, tickers):
    df_preco_corrigido = pegar_df_preco_corrigido(data_ini, data_fim, tickers)
    return df_preco_corrigido


def gerar_grafico_precos_diversos(data_ini, data_fim, tickers):
    df_preco_diversos = pegar_df_preco_diversos(data_ini, data_fim, tickers)
    return df_preco_diversos


def calcular_rendimento_acoes(dados_preco):
    df_rendimento = calcular_rendimento(dados_preco)
    return df_rendimento


def analisar_roe_acoes(dados_planilhao):
    df_roe = analisar_roe(dados_planilhao)
    return df_roe


def analisar_magic_formula_acoes(dados_planilhao):
    df_magic_formula = analisar_magic_formula(dados_planilhao)
    return df_magic_formula
