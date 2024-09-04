import yt_dlp
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def download_youtube_video(url, output_path='.'):
    try:
        # Options for yt-dlp
        ydl_opts = {
            'format': 'best',  # Download the best quality available
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Output template for downloaded files
        }

        # Download the video using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download completed!")
    except Exception as e:
        print(f"An error occurred: {e}")

def on_submit():
    url = entry_url.get()
    output_path = entry_output.get() 
    download_youtube_video(url, output_path)

def browse_directory():
    """Open a file dialog to select the output directory."""
    directory = filedialog.askdirectory()
    if directory:
        entry_output.delete(0, tk.END)  # Clear the current entry
        entry_output.insert(0, directory)  # Insert the selected directory

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

root = tk.Tk()
root.title("Baixa Video")

window_width = 500
window_height = 150

center_window(root, window_width, window_height)

# Configure the root grid
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Configure the frame grid to center the content
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

# Define the URL input
ttk.Label(frame, text="URL / https:").grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
entry_url = ttk.Entry(frame, width='50')
entry_url.grid(row=0, column=1, sticky=(tk.W, tk.E), pady='2')

# Define the output directory input
ttk.Label(frame, text="Salvar em :").grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
entry_output = ttk.Entry(frame)
entry_output.grid(row=1, column=1, sticky=(tk.W, tk.E), pady='2')

browse_button = ttk.Button(frame, text="Procurar", command=browse_directory)
browse_button.grid(row=1, column=2, padx="5")

submit_button = ttk.Button(frame, text="Download", command=on_submit)
submit_button.grid(row=2, column=0, columnspan=3, pady="10")

root.mainloop()
