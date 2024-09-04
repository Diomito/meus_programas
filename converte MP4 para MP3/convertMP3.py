from pydub import AudioSegment
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def select_file():
    """Open a file dialog to select an MP4 file."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select an MP4 file",
        filetypes=[("MP4 files", "*.mp4")]
    )
    return file_path

def convert_mp4_to_mp3(input_file, output_file):
    """Convert an MP4 file to an MP3 file."""
    try:
        # Load the MP4 file
        audio = AudioSegment.from_file(input_file, format="mp4")
        
        # Export as MP3
        audio.export(output_file, format="mp3")
        
        print(f"Conversion completed successfully! Saved as {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

def ask_convert_another():
    """Display a dialog asking if the user wants to convert another song."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    return messagebox.askyesno("Convert Another", "Do you want to convert another song?")

if __name__ == "__main__":
    while True:
        # Select the input MP4 file
        input_file = select_file()
        
        if input_file:
            # Define the output MP3 file path
            base = os.path.splitext(input_file)[0]
            output_file = base + ".mp3"
            
            # Convert the selected file to MP3
            convert_mp4_to_mp3(input_file, output_file)
            
            # Ask if the user wants to convert another file
            if not ask_convert_another():
                break
        else:
            print("No file was selected.")
            break
