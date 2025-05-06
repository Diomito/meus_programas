import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip

def convert_mov_to_mp4():
    # Open file dialog to select multiple MOV files
    input_files = filedialog.askopenfilenames(
        title="Select MOV Files",
        filetypes=[("MOV Files", "*.mov")]
    )
    if not input_files:
        return  # No files selected

    # Convert each selected file
    for input_file in input_files:
        output_file = input_file.rsplit(".", 1)[0] + ".mp4"
        try:
            clip = VideoFileClip(input_file)
            clip.write_videofile(output_file, codec="libx264")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred with {input_file}: {e}")

    # Ask if the user wants to convert more files
    retry = messagebox.askyesno("Convert More?", "Do you want to convert more files?")
    if retry:
        convert_mov_to_mp4()

# Create the main application window
root = tk.Tk()
root.title("MOV to MP4 Converter")
root.geometry("300x150")

# Create and place the convert button
convert_button = tk.Button(root, text="Convert MOV to MP4", command=convert_mov_to_mp4)
convert_button.pack(expand=True)

# Run the application
root.mainloop()
