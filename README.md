# AP2 - Projeto de Ciência de Dados

## Descrição
Este projeto é uma aplicação web desenvolvida com Streamlit para análise de ações. A aplicação permite consultar dados de preços históricos, calcular rendimentos, gerar gráficos e aplicar estratégias de investimento baseadas em indicadores fundamentalistas.

## Funcionalidades
- **Consulta de Planilhão**: Consulta todas as ações com os principais indicadores fundamentalistas.
- **Geração de Estratégias**: Gera estratégias de investimento baseadas em indicadores de rentabilidade e desconto.
- **Gráficos de Ações**: Gera gráficos de preços históricos, retornos diários e matriz de correlação para uma lista de tickers.

Estrutura do Projeto
- app.py: Arquivo principal que gerencia a navegação entre as páginas.
- setup_paths.py: Configuração dos diretórios e logging.
- frontend/: Contém as páginas da aplicação.
- - planilhao_page.py: Página de consulta do planilhão.
- - estrategia_page.py: Página de geração de estratégias.
- - grafico_page.py: Página de gráficos de ações.
- backend/: Contém as APIs e funções auxiliares.
- - apis.py: Funções para consulta de dados de APIs.
- - views.py: Funções para processamento e análise de dados.