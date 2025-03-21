import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from client import request_file, send_script

RECEIVED_DIR = 'data'

def update_image():
    request_file("GET_IMAGE")
    image_path = os.path.join(RECEIVED_DIR, "screen.png")

    if os.path.exists(image_path):
        img = Image.open(image_path)
        img_width, img_height = img.size

        # Maintain aspect ratio
        max_width, max_height = 800, 450
        ratio = min(max_width / img_width, max_height / img_height)
        new_width, new_height = int(img_width * ratio), int(img_height * ratio)

        img = img.resize((new_width, new_height))
        img = ImageTk.PhotoImage(img)

        canvas.create_image(0, 0, anchor=tk.NW, image=img)
        canvas.image = img  # Keep reference to avoid garbage collection
    else:
        messagebox.showerror("Error", "Image not found!")

def download_csv():
    request_file("GET_CSV")
    messagebox.showinfo("Download Complete", "CSV file downloaded successfully!")

def load_script():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            script_text.delete("1.0", tk.END)
            script_text.insert(tk.END, file.read())

def send_script_to_server():
    script_content = script_text.get("1.0", tk.END).strip()
    if not script_content:
        messagebox.showwarning("Warning", "Script is empty!")
        return

    temp_script_path = os.path.join(RECEIVED_DIR, "script.txt")
    with open(temp_script_path, 'w') as f:
        f.write(script_content)

    send_script(temp_script_path)
    messagebox.showinfo("Script Sent", "SCPI script sent successfully!")

def request_console():
    """Requests and displays the console log from the server."""
    request_file("GET_CONSOLE")
    log_path = os.path.join(RECEIVED_DIR, "console.log")

    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            console_text.delete("1.0", tk.END)
            console_text.insert(tk.END, f.read())
    else:
        messagebox.showerror("Error", "Console log not found!")

def clear_console():
    """Clears the console output display."""
    console_text.delete("1.0", tk.END)

root = tk.Tk()
root.title("TinySA Client")

# Frame for image and buttons
frame = tk.Frame(root, padx=20, pady=20)
frame.grid(row=0, column=0, sticky="nsew")

# Canvas for image display
canvas = tk.Canvas(frame, width=800, height=450)
canvas.grid(row=0, column=0, padx=10, pady=10)

# Button Frame
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, padx=20, pady=20)

update_btn = tk.Button(button_frame, text="Update Image", command=update_image, width=20, height=2, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
update_btn.grid(row=0, column=0, padx=10, pady=10)

download_btn = tk.Button(button_frame, text="Download CSV", command=download_csv, width=20, height=2, bg="#2196F3", fg="white", font=("Arial", 12, "bold"))
download_btn.grid(row=1, column=0, padx=10, pady=10)

# Script Frame
script_frame = tk.Frame(root, padx=20, pady=20)
script_frame.grid(row=2, column=0, padx=20, pady=20)

script_text = tk.Text(script_frame, height=10, width=50, font=("Arial", 12), bd=2)
script_text.grid(row=0, column=0, padx=10, pady=10)

load_btn = tk.Button(script_frame, text="Load Script", command=load_script, width=20, height=2, bg="#FF9800", fg="white", font=("Arial", 12, "bold"))
load_btn.grid(row=1, column=0, padx=10, pady=10)

send_btn = tk.Button(script_frame, text="Send Script", command=send_script_to_server, width=20, height=2, bg="#F44336", fg="white", font=("Arial", 12, "bold"))
send_btn.grid(row=2, column=0, padx=10, pady=10)

# Console Frame
console_frame = tk.Frame(root, padx=20, pady=20)
console_frame.grid(row=3, column=0, padx=20, pady=20)

console_label = tk.Label(console_frame, text="Console Output", font=("Arial", 12, "bold"))
console_label.grid(row=0, column=0, padx=10, pady=5)

console_text = tk.Text(console_frame, height=10, width=50, font=("Arial", 12), bd=2, bg="black", fg="white")
console_text.grid(row=1, column=0, padx=10, pady=10)

console_btn_frame = tk.Frame(console_frame)
console_btn_frame.grid(row=2, column=0, pady=10)

refresh_console_btn = tk.Button(console_btn_frame, text="Refresh Console", command=request_console, width=15, height=2, bg="#9C27B0", fg="white", font=("Arial", 12, "bold"))
refresh_console_btn.grid(row=0, column=0, padx=5)

clear_console_btn = tk.Button(console_btn_frame, text="Clear Console", command=clear_console, width=15, height=2, bg="#FF5722", fg="white", font=("Arial", 12, "bold"))
clear_console_btn.grid(row=0, column=1, padx=5)

# Configure grid weights for responsive layout
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=0)
root.grid_columnconfigure(0, weight=1)

root.mainloop()
