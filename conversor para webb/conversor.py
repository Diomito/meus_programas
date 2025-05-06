import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def convert_to_webp():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg; .heic")])
    if not file_path:
        return
    
    try:
        with Image.open(file_path) as img:
            webp_path = file_path.rsplit(".", 1)[0] + ".jpg"
            img.save(webp_path, "jpg")
            messagebox.showinfo("Conversion Successful", f"Image converted and saved as {webp_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.geometry('200x100')
root.title("Converter Imagem")

convert_button = tk.Button(root, text="Convert to WebP", command=convert_to_webp)
convert_button.pack(pady=20, padx=20)

root.mainloop()