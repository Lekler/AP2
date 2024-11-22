import logging
import sys
from pathlib import Path

# Define o diretório base e os diretórios frontend e backend
BASE_DIR = Path(__file__).resolve().parent
FRONT_DIR = BASE_DIR / 'frontend'
BACK_DIR = BASE_DIR / 'backend'

# Cria os diretórios se não existirem
FRONT_DIR.mkdir(exist_ok=True)
BACK_DIR.mkdir(exist_ok=True)

# Adiciona os diretórios ao sys.path
sys.path.append(str(BASE_DIR))
sys.path.append(str(FRONT_DIR))
sys.path.append(str(BACK_DIR))

# Configuração básica do logging
LOG_DIR = BACK_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(f'{LOG_DIR}/app.log', mode='a'),
                        logging.StreamHandler()
                    ])
