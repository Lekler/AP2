import requests
import logging
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")
headers = {"Authorization": "JWT {}".format(token)}

logger = logging.getLogger(__name__)


def pegar_planilhao(data_base):
    params = {'data_base': data_base}
    try:
        r = requests.get(
            'https://laboratoriodefinancas.com/api/v1/planilhao', params=params, headers=headers)
        if r.status_code == 200:
            dados = r.json()
            logger.info(
                f"Dados do Planilhao consultados com sucesso: {data_base}")
            return dados
        else:
            logger.error(f"Erro na consulta do planilhao: {data_base}")
    except Exception as e:
        logger.error(f"ERRO TECNICO: {e}")


def get_preco_corrigido(data_ini, data_fim, ticker):
    params = {
        'ticker': ticker,
        'data_ini': data_ini,
        'data_fim': data_fim
    }
    try:
        r = requests.get(
            'https://laboratoriodefinancas.com/api/v1/preco-corrigido', params=params, headers=headers)
        if r.status_code == 200:
            dados = r.json()
            logger.info(
                f"Dados do Preco Corrigido consultados com sucesso: {ticker}")
            return dados
        else:
            logger.error(f"Erro na consulta do Preco Corrigido: {ticker}")
    except Exception as e:
        logger.error(f"ERRO TECNICO: {e}")


def get_preco_diversos(data_ini, data_fim, ticker):
    params = {
        'ticker': ticker,
        'data_ini': data_ini,
        'data_fim': data_fim
    }
    try:
        r = requests.get(
            'https://laboratoriodefinancas.com/api/v1/preco-diversos', params=params, headers=headers)
        if r.status_code == 200:
            dados = r.json()
            logger.info(
                f"Dados do Preco diversos consultados com sucesso: {ticker}")
            return dados
        else:
            logger.error(f"Erro na consulta do Preco diversos: {ticker}")
    except Exception as e:
        logger.error(f"ERRO TECNICO: {e}")


def obter_preco_acoes(ticker, data_ini, data_fim):
    params = {
        'ticker': ticker,
        'data_ini': data_ini,
        'data_fim': data_fim
    }
    try:
        r = requests.get(
            'https://laboratoriodefinancas.com/api/v1/preco-acoes', params=params, headers=headers)
        if r.status_code == 200:
            dados = r.json()
            logger.info(
                f"Dados do Preco Acoes consultados com sucesso: {ticker}")
            return dados
        else:
            logger.error(f"Erro na consulta do Preco Acoes: {
                         ticker} - Status Code: {r.status_code} - Response: {r.text}")
    except Exception as e:
        logger.error(f"ERRO TECNICO: {e}")
