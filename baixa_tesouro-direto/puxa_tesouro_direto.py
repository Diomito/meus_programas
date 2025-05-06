from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Caminho do GeckoDriver e do Firefox
driver_path = r"D:\Files\my programs\baixa_tesouro-direto\geckodriver.exe"  # Usando raw string
firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"  # Caminho completo para o Firefox

# Configuração do serviço do GeckoDriver
service = Service(driver_path)

# Configuração das opções do Firefox
options = Options()
options.binary = firefox_path  # Define o caminho do binário do Firefox

# Inicia o navegador Firefox com o serviço e opções configuradas
driver = webdriver.Firefox(service=service, options=options)
driver.get("https://www.tesourodireto.com.br/titulos/precos-e-taxas.htm")

# Espera até que a tabela esteja presente (aumentando o tempo para 20 segundos)
wait = WebDriverWait(driver, 20)
try:
    tabela = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.td-invest-table")))
except Exception as e:
    print(f"Erro ao encontrar a tabela: {e}")
    driver.quit()
    exit()

# Lista para armazenar os dados
dados = []

# Encontra todos os tbody dentro da tabela (cada título)
titulos = tabela.find_elements(By.TAG_NAME, "tbody")

for titulo in titulos:
    try:
        # Extrai os dados de cada título
        nome = titulo.find_element(By.CLASS_NAME, "td-invest-table__name__text").text
        rentabilidade = titulo.find_elements(By.CLASS_NAME, "td-invest-table__col__text")[0].text
        valor_titulo = titulo.find_elements(By.CLASS_NAME, "td-invest-table__col__text")[2].text
        vencimento = titulo.find_elements(By.CLASS_NAME, "td-invest-table__col__text")[3].text

        # Adiciona os dados à lista
        dados.append({
            "Nome do Título": nome,
            "Rentabilidade Anual": rentabilidade,
            "Valor do Titulo": valor_titulo,
            "Data de Vencimento": vencimento
        })
    except Exception as e:
        print(f"Erro ao processar um título: {e}")

# Fecha o navegador
driver.quit()

# Cria o DataFrame e salva no Excel
df = pd.DataFrame(dados)
df.to_excel("tesouro_direto_titulos.xlsx", index=False)

print("Dados salvos com sucesso no arquivo 'tesouro_direto_titulos.xlsx'!")
