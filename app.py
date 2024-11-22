import setup_paths  # Certifique-se de que setup_paths.py está configurado corretamente
import streamlit as st
from multiapp import MultiApp
from frontend import planilhao_page, estrategia_page, grafico_page

app = MultiApp()

# Adicionar todas as páginas
app.add_app("PLANILHAO", planilhao_page.app)
app.add_app("Estrategia", estrategia_page.app)
app.add_app("Grafico", grafico_page.app)

# Executar a aplicação
app.run()
