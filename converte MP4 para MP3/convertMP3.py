from pydub import AudioSegment
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def select_files():
    """Open a file dialog to select multiple MP4 files."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_paths = filedialog.askopenfilenames(
        title="Select MP4 files",
        filetypes=[("MP4 files", "*.mp4")]
    )
    return file_paths

def convert_mp4_to_mp3(input_file, output_file):
    """Convert an MP4 file to an MP3 file."""
    try:
        # Load the MP4 file
        audio = AudioSegment.from_file(input_file, format="mp4")
        
        # Export as MP3
        audio.export(output_file, format="mp3")
        return True
    except Exception as e:
        print(f"An error occurred with {input_file}: {e}")
        return False

def ask_convert_another():
    """Display a dialog asking if the user wants to convert more files."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    return messagebox.askyesno("Convert Another", "Do you want to convert more files?")

def show_conversion_complete():
    """Display a dialog indicating the conversion is complete."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Conversion Complete", "All selected files have been successfully converted!")

if __name__ == "__main__":
    while True:
        # Select the input MP4 files
        input_files = select_files()
        
        if input_files:
            for input_file in input_files:
                # Define the output MP3 file path
                base = os.path.splitext(input_file)[0]
                output_file = base + ".mp3"
                
                # Convert the selected file to MP3
                if convert_mp4_to_mp3(input_file, output_file):
                    print(f"Conversion completed successfully! Saved as {output_file}")
            
            # Notify the user that all conversions are complete
            show_conversion_complete()
            
            # Ask if the user wants to convert more files
            if not ask_convert_another():
                break
        else:
            print("No files were selected.")
            break