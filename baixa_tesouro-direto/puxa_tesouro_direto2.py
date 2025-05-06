import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re

# Função para escolher o diretório
def escolher_diretorio():
    root = tk.Tk()
    root.title("Escolher Diretório") 
    root.geometry("300x100")
    root.update()
    diretorio = filedialog.askdirectory(title="Escolha o diretório para salvar o arquivo")
    root.quit()
    return diretorio

# Caminho do GeckoDriver e do Firefox
driver_path = r"D:\Files\my programs\baixa_tesouro-direto\geckodriver.exe"  # Usando raw string
firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"  # Caminho completo para o Firefox

service = Service(driver_path)

# Configuração das opções do Firefox
options = Options()
options.binary = firefox_path  # Define o caminho do binário do Firefox

# Inicia o navegador Firefox com o serviço e opções configuradas
driver = webdriver.Firefox(service=service, options=options)
driver.get("https://www.tesourodireto.com.br/titulos/precos-e-taxas.htm")

# Espera até que a tabela esteja visível (aumentando o tempo para 30 segundos)
wait = WebDriverWait(driver, 30)
try:
    # Tente encontrar a tabela com um seletor mais genérico ou alterado
    tabela = wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'td-invest-table')]")))
except Exception as e:
    print(f"Erro ao encontrar a tabela: {e}")
    driver.quit()
    exit()

# Lista para armazenar os dados
dados = []

# Encontra todos os tbody dentro da tabela (cada título)
titulos = tabela.find_elements(By.TAG_NAME, "tbody")


# Função para extrair apenas o valor percentual
def extrair_porcentagem(rentabilidade):
    # Regex para extrair o valor percentual (ex: "0,0472%" ou "SELIC + 0,0472%")
    match = re.search(r'([0-9,]+)%', rentabilidade)
    if match:
        return match.group(1) + "%"
    return rentabilidade 

# Dentro do loop de extração dos dados:
for titulo in titulos:
    try:
        # Extrai os dados de cada título
        nome = titulo.find_element(By.CLASS_NAME, "td-invest-table__name__text").text
        rentabilidade = titulo.find_elements(By.CLASS_NAME, "td-invest-table__col__text")[0].text
        valor_titulo = titulo.find_elements(By.CLASS_NAME, "td-invest-table__col__text")[2].text
        vencimento = titulo.find_elements(By.CLASS_NAME, "td-invest-table__col__text")[3].text
        
        # Limpa a rentabilidade, mantendo apenas a porcentagem
        rentabilidade = extrair_porcentagem(rentabilidade)

        # Adiciona os dados à lista
        dados.append({
            "Nome do Título": nome,
            "Rentabilidade Anual": rentabilidade,
            "Valor do Titulo": valor_titulo,
            "Data de Vencimento": vencimento
        })
    except Exception as e:
        print(f"Erro ao processar um título: {e}")

driver.quit()

diretorio = escolher_diretorio()

if diretorio:
    caminho_arquivo = f"{diretorio}/tesouro_direto_titulos.xlsx"
    df = pd.DataFrame(dados)
    df.to_excel(caminho_arquivo, index=False)
    print(f"Dados salvos com sucesso no arquivo '{caminho_arquivo}'!")
else:
    print("Nenhum diretório selecionado. O arquivo não foi salvo.")