import pandas as pd
from datetime import date
import logging
import re
import matplotlib.pyplot as plt
import seaborn as sns
from backend.apis import (
    get_preco_diversos, pegar_planilhao, get_preco_corrigido)

logger = logging.getLogger(__name__)


def filtrar_duplicado(df: pd.DataFrame, meio: str = None) -> pd.DataFrame:
    """
    Filtra o df das ações duplicados baseado no meio escolhido (default: volume)

    params:
    df (pd.DataFrame): dataframe com os ticker duplicados 
    meio (str): campo escolhido para escolher qual ticker escolher (default: volume)

    return:
    (pd.DataFrame): dataframe com os ticker filtrados.
    """
    meio = meio or 'volume'
    df_dup = df[df.empresa.duplicated(keep=False)]
    lst_dup = df_dup.empresa.unique()
    lst_final = []
    for tic in lst_dup:
        tic_dup = df_dup[df_dup.empresa == tic].sort_values(
            by=[meio], ascending=False)['ticker'].values[0]
        lst_final = lst_final + [tic_dup]
    lst_dup = df_dup[~df_dup.ticker.isin(lst_final)]['ticker'].values
    logger.info(f"Ticker Duplicados Filtrados: {lst_dup}")
    print(f"Ticker Duplicados Filtrados: {lst_dup}")
    return df[~df.ticker.isin(lst_dup)]


def pegar_df_planilhao(data_base: date) -> pd.DataFrame:
    """
    Consulta todas as ações com os principais indicadores fundamentalistas

    params:
    data_base (date): Data Base para o cálculo dos indicadores.

    return:
    df (pd.DataFrame): DataFrame com todas as Ações.
    """
    dados = pegar_planilhao(data_base)
    if dados:
        dados = dados['dados']
        planilhao = pd.DataFrame(dados)
        planilhao['empresa'] = [ticker[:4]
                                for ticker in planilhao.ticker.values]
        df = filtrar_duplicado(planilhao)
        logger.info(f"Dados do Planilhao consultados com sucesso: {data_base}")
        print(f"Dados do Planilhao consultados com sucesso: {data_base}")
        return df
    else:
        logger.info(f"Sem Dados no Planilhão: {data_base}")
        print(f"Sem Dados no Planilhão: {data_base}")
        return None


def gerar_estrategia(data_base, ind_rentabilidade, ind_desconto, qtde_acoes):
    df = pegar_df_planilhao(data_base)
    if df is not None:
        df = df[["ticker", ind_rentabilidade, ind_desconto]]
        df["rank_rent"] = df[ind_rentabilidade].rank()
        df["rank_desc"] = df[ind_desconto].rank()
        df["rank_final"] = df["rank_rent"] + df["rank_desc"]
        df = df.sort_values(["rank_final"], ascending=False).reset_index(
            drop=True)[:qtde_acoes]
        return df
    else:
        return None


def pegar_df_preco_corrigido(data_ini: date, data_fim: date, carteira: list, top_n: int = 10) -> pd.DataFrame:
    """
    Consulta os preços Corrigidos de uma lista de ações

    params:
    data_ini (date): data inicial da consulta
    data_fim (date): data final da consulta
    carteira (list): lista de ativos a serem consultados
    top_n (int): número de ativos a serem consultados (default: 10)

    return:
    df_preco (pd.DataFrame): dataframe com os preços do período dos ativos da lista
    """
    df_preco = pd.DataFrame()
    carteira = carteira[:top_n]  # Seleciona os top_n tickers
    for ticker in carteira:
        dados = get_preco_corrigido(data_ini, data_fim, ticker)
        if dados:
            dados = dados['dados']
            df_temp = pd.DataFrame.from_dict(dados)
            # Converter a coluna 'data' para datetime
            df_temp['data'] = pd.to_datetime(df_temp['data'])
            df_preco = pd.concat([df_preco, df_temp],
                                 axis=0, ignore_index=True)
            logger.info(f'{ticker} finalizado!')
            print(f'{ticker} finalizado!')
        else:
            logger.error(f"Sem Preco Corrigido: {ticker}")
            print(f"Sem Preco Corrigido: {ticker}")
    return df_preco


def pegar_df_preco_diversos(data_ini: date, data_fim: date, carteira: list, top_n: int = 10) -> pd.DataFrame:
    """
    Consulta os preços históricos de uma carteira de ativos

    params:
    data_ini (date): data inicial da consulta
    data_fim (date): data final da consulta
    carteira (list): lista de ativos a serem consultados
    top_n (int): número de ativos a serem consultados (default: 10)

    return:
    df_preco (pd.DataFrame): dataframe com os preços do período dos ativos da lista
    """
    df_preco = pd.DataFrame()
    carteira = carteira[:top_n]  # Seleciona os top_n tickers
    for ticker in carteira:
        dados = get_preco_diversos(data_ini, data_fim, ticker)
        if dados:
            dados = dados['dados']
            df_temp = pd.DataFrame.from_dict(dados)
            # Converter a coluna 'data' para datetime
            df_temp['data'] = pd.to_datetime(df_temp['data'])
            df_preco = pd.concat([df_preco, df_temp],
                                 axis=0, ignore_index=True)
            logger.info(f'{ticker} finalizado!')
            print(f'{ticker} finalizado!')
        else:
            logger.error(f"Sem Preco Corrigido: {ticker}")
            print(f"Sem Preco Corrigido: {ticker}")
    return df_preco


def gerar_grafico(data_ini, data_fim, carteira):
    # carteira = ["PETR4", "VALE3", "BBAS3"]
    # data_ini=date(2000,1,1)
    # data_fim=date(2024,11,1)
    df_preco = pegar_df_preco_corrigido(data_ini, data_fim, carteira)
    df_grafico = df_preco.groupby("data")["fechamento"].sum()

    df_grafico.index
    df_grafico.values
    sns.lineplot(df_grafico)
    plt.figure()

    plt.plot(df_grafico)


def calcular_rendimento(df):
    """Função para calcular o rendimento percentual de uma ação."""
    if isinstance(df, list):
        df = pd.DataFrame(df)
    df['data'] = pd.to_datetime(df['data'])
    df = df.sort_values(by='data')
    df.set_index('data', inplace=True)
    df['retorno'] = df['fechamento'].pct_change()
    return df


def analisar_roe(dados_planilhao):
    """Análise ROE das ações."""
    df_planilhao = pd.DataFrame(dados_planilhao)
    df_roe = df_planilhao[['ticker', 'roe', 'volume']].copy()
    df_roe['nome_base'] = df_roe['ticker'].apply(
        lambda x: re.sub(r'\d+$', '', x))
    df_roe_filtrado = df_roe.loc[df_roe.groupby(
        'nome_base')['volume'].idxmax()].copy()
    return df_roe_filtrado[['ticker', 'roe']].sort_values(by='roe', ascending=False).head(10)


def analisar_magic_formula(dados_planilhao):
    """Análise de Magic Formula das ações."""
    df_magic = pd.DataFrame(dados_planilhao)[
        ['setor', 'ticker', 'roic', 'earning_yield', 'volume']].copy()
    df_magic['nome_base'] = df_magic['ticker'].apply(
        lambda x: re.sub(r'\d+$', '', x))
    df_magic_filtrado = df_magic.loc[df_magic.groupby(
        'nome_base')['volume'].idxmax()].copy()
    setores_remover = ['bancos', 'seguros', 'financeiros']
    df_magic_filtrado = df_magic_filtrado.loc[~df_magic_filtrado['setor'].str.lower(
    ).isin(setores_remover)].copy()
    df_magic_filtrado = df_magic_filtrado.dropna(
        subset=['roic', 'earning_yield'])
    df_magic_filtrado['ranking_roic'] = df_magic_filtrado['roic'].rank(
        ascending=False)
    df_magic_filtrado['ranking_earning_yield'] = df_magic_filtrado['earning_yield'].rank(
        ascending=False)
    df_magic_filtrado['ranking_combined'] = df_magic_filtrado['ranking_roic'] + \
        df_magic_filtrado['ranking_earning_yield']
    return df_magic_filtrado.sort_values(by='ranking_combined').head(10)
