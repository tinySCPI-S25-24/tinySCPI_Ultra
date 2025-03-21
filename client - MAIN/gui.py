import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from client import request_file, send_script

RECEIVED_DIR = 'data'


def update_image():
    request_file("GET_IMAGE")
    image_path = os.path.join(RECEIVED_DIR, "screen.jpg")

    if os.path.exists(image_path):
        img = Image.open(image_path)
        img_width, img_height = img.size

        # Maintain the aspect ratio (scale the image to fit 800x450)
        max_width = 800
        max_height = 450
        ratio = min(max_width / img_width, max_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)

        img = img.resize((new_width, new_height))
        img = ImageTk.PhotoImage(img)

        # Display the image on the canvas
        canvas.create_image(0, 0, anchor=tk.NW, image=img)
        canvas.image = img  # Keep a reference to avoid garbage collection
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


root = tk.Tk()
root.title("TinySA Client")

# Create a frame for the image and button layout
frame = tk.Frame(root, padx=20, pady=20)
frame.grid(row=0, column=0, sticky="nsew")

# Create a canvas to display the image
canvas = tk.Canvas(frame, width=800, height=450)
canvas.grid(row=0, column=0, padx=10, pady=10)

# Buttons
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, padx=20, pady=20)

update_btn = tk.Button(button_frame, text="Update Image", command=update_image, width=20, height=2, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
update_btn.grid(row=0, column=0, padx=10, pady=10)

download_btn = tk.Button(button_frame, text="Download CSV", command=download_csv, width=20, height=2, bg="#2196F3", fg="white", font=("Arial", 12, "bold"))
download_btn.grid(row=1, column=0, padx=10, pady=10)

# Script area
script_frame = tk.Frame(root, padx=20, pady=20)
script_frame.grid(row=2, column=0, padx=20, pady=20)

script_text = tk.Text(script_frame, height=10, width=50, font=("Arial", 12), bd=2)
script_text.grid(row=0, column=0, padx=10, pady=10)

load_btn = tk.Button(script_frame, text="Load Script", command=load_script, width=20, height=2, bg="#FF9800", fg="white", font=("Arial", 12, "bold"))
load_btn.grid(row=1, column=0, padx=10, pady=10)

send_btn = tk.Button(script_frame, text="Send Script", command=send_script_to_server, width=20, height=2, bg="#F44336", fg="white", font=("Arial", 12, "bold"))
send_btn.grid(row=2, column=0, padx=10, pady=10)

# Configure grid weights for responsive layout
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_columnconfigure(0, weight=1)

root.mainloop()
