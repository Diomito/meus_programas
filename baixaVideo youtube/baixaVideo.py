import yt_dlp
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


def download_youtube_videos(urls, output_path='.'):
    skipped = []  # List to store skipped videos
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'ignoreerrors': True,  # Ignore errors and continue
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for url in urls:
                try:
                    ydl.download([url])  # Attempt to download each URL individually
                except yt_dlp.utils.DownloadError as e:
                    skipped.append((url, str(e)))  # Log skipped videos
    except Exception as e:
        skipped.append((None, str(e)))  # Handle unexpected global errors

    return skipped


def show_message(title, message):
    """Display a message in a pop-up window."""
    messagebox.showinfo(title, message)


def on_submit():
    """Get user input and start downloading."""
    urls = entry_url.get("1.0", tk.END).strip().splitlines()  # Retrieve all URLs from the Text widget
    output_path = entry_output.get().strip()

    if not urls:
        show_message("Error", "Please enter at least one valid URL.")
        return

    if not output_path:
        show_message("Error", "Please select an output directory.")
        return

    # Call the download function and capture skipped videos
    skipped = download_youtube_videos(urls, output_path)

    if skipped:
        skipped_message = "\n".join([f"{url} - {error}" for url, error in skipped if url])
        show_message("Completed with Errors", f"The following videos were skipped:\n{skipped_message}")
    else:
        show_message("Success", "All videos downloaded successfully!")


def browse_directory():
    """Open a dialog to select the output directory."""
    directory = filedialog.askdirectory()
    if directory:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, directory)


def center_window(root, width, height):
    """Center the main window on the screen."""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')


# Main window configuration
root = tk.Tk()
root.title("YouTube Video Downloader")

window_width = 500
window_height = 300  # Increased height to accommodate multi-line input
center_window(root, window_width, window_height)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=3)

# URL Entry
ttk.Label(frame, text="URL(s):").grid(row=0, column=0, sticky=tk.W, pady=5)
entry_url = tk.Text(frame, height=10, width=50)  # Multi-line text widget for multiple URLs
entry_url.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)

# Output Directory Entry
ttk.Label(frame, text="Save to:").grid(row=1, column=0, sticky=tk.W, pady=5)
entry_output = ttk.Entry(frame)
entry_output.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

browse_button = ttk.Button(frame, text="Browse", command=browse_directory)
browse_button.grid(row=1, column=2, padx=5)

# Download Button
submit_button = ttk.Button(frame, text="Download", command=on_submit)
submit_button.grid(row=2, column=0, columnspan=3, pady=10)

root.mainloop()