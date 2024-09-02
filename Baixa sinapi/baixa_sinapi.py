import requests
import zipfile
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import time

def download_and_extract(ano, mes, estado, tipo):
    file_url = f"https://www.caixa.gov.br/Downloads/sinapi-a-partir-jul-2009-{estado.lower()}/SINAPI_ref_Insumos_Composicoes_{estado.upper()}_{ano}{mes}_{tipo}.zip"
    zip_file_path = f"SINAPI_{estado.upper()}_{tipo}_{ano}{mes}.zip"
    extract_folder = f"SINAPI_{estado.upper()}_{tipo}_{ano}{mes}"

    max_retries = 5
    backoff_factor = 1

    for attempt in range(max_retries):
        try:
            response = requests.get(file_url, stream=True)
            response.raise_for_status()

            with open(zip_file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_folder)

            os.remove(zip_file_path)
            messagebox.showinfo("Success", "Download and extraction complete.")
            return

        except requests.exceptions.RequestException as e:
            if response.status_code == 429:
                wait = backoff_factor * (2 ** attempt)
                print(f"Rate limit exceeded. Waiting {wait} seconds before retrying...")
                time.sleep(wait)
            else:
                messagebox.showerror("Error", f"Failed to download file: {e}")
                return
        except zipfile.BadZipFile as e:
            messagebox.showerror("Error", f"Failed to extract ZIP file: {e}")
            return
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            return

    messagebox.showerror("Error", "Max retries exceeded. Please try again later.")

def on_submit():
    ano = entry_ano.get()
    mes = entry_mes.get()
    estado = entry_estado.get().upper()
    tipo = entry_tipo.get()
    download_and_extract(ano, mes, estado, tipo)

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

root = tk.Tk()
root.title("SINAPI Download")

window_width = 300
window_height = 180

center_window(root, window_width, window_height)

# Configure the root grid
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

frame = ttk.Frame(root, padding="10",)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Configure the frame grid to center the content
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

# Define as entradas dos dados ANO
ttk.Label(frame, text="Ano:").grid(row=0, column=0, sticky=tk.W)
entry_ano = ttk.Entry(frame)
entry_ano.grid(row=0, column=1, sticky=(tk.W, tk.E), pady='2')

# Define as entradas dos dados MES
ttk.Label(frame, text="Mês:").grid(row=1, column=0, sticky=tk.W)
entry_mes = ttk.Entry(frame)
entry_mes.grid(row=1, column=1, sticky=(tk.W, tk.E), pady='2')

# Define o ESTADO
ttk.Label(frame, text="Estado:").grid(row=2, column=0, sticky=tk.W, pady='2', padx='2')
estado_values = ["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR","RS", "SC", "SE", "SP", "TO"]
entry_estado = ttk.Combobox(frame, values=estado_values)
entry_estado.grid(row=2, column=1, sticky=(tk.W, tk.E), pady='2', padx='2')

# Define o TIPO
ttk.Label(frame, text="Tipo:").grid(row=3, column=0, sticky=tk.W, pady='2', padx='2')
tipo_values = ["Naodesonerado", "Desonerado"]
entry_tipo = ttk.Combobox(frame, values=tipo_values)
entry_tipo.grid(row=3, column=1, sticky=(tk.W, tk.E), pady='2', padx='2')

submit_button = ttk.Button(frame, text="Download", command=on_submit)
submit_button.grid(row=4, column=0, columnspan=2, pady="10")

root.mainloop()