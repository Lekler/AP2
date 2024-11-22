# import os
# from pathlib import Path
# BASE_DIR = Path(__file__).parent.parent
# BACK_DIR = str(BASE_DIR) + '/backend'
# FRONT_DIR = str(BASE_DIR) + '/frontend'
# LOG_DIR = str(BACK_DIR) + '/logs'
# import logging # Configuração básica do logging
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     filename=f'{LOG_DIR}/app.log',  # Nome do arquivo de log
#                     filemode='a') 

from dotenv import load_dotenv
import os
from pathlib import Path
import logging

# Definir os diretórios do projeto
BASE_DIR = Path(__file__).parent.parent
BACK_DIR = BASE_DIR / 'backend'
FRONT_DIR = BASE_DIR / 'frontend'
LOG_DIR = BACK_DIR / 'logs'

# Configuração de logging
os.makedirs(LOG_DIR, exist_ok=True)  # Criar o diretório de logs se não existir
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=LOG_DIR / 'app.log',  # Nome do arquivo de log
    filemode='a'
)

# Variáveis de ambiente
load_dotenv()  # Carregar variáveis do arquivo .env

TOKEN = os.getenv('TOKEN')  # Token da API
