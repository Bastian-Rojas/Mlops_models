import tkinter as tk
from tkinter import filedialog
import os
from model_loader import load_model
from video_processor import process_video
from image_processor import process_images

# Cargar el modelo YOLO
model = load_model("best.pt")

def select_video():
    video_path = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="Seleccionar Video",
        filetypes=[("Video files", "*.mp4;*.avi;*.mov")],
        parent=root
    )
    if video_path:
        process_video(video_path, model)

def select_directory():
    directory_path = filedialog.askdirectory(
        initialdir=os.getcwd(),
        title="Seleccionar Directorio de Imágenes",
        parent=root
    )
    if directory_path:
        process_images(directory_path, model)

def close_app():
    root.destroy()

root = tk.Tk()
root.title("Vaquitas")

# Configurar tamaño mínimo de la ventana principal
root.minsize(400, 200)

btn_video = tk.Button(root, text="Seleccionar Video", command=select_video)
btn_video.pack(pady=10)

btn_images = tk.Button(root, text="Seleccionar Directorio de Imágenes", command=select_directory)
btn_images.pack(pady=10)

btn_close = tk.Button(root, text="Cerrar", command=close_app)
btn_close.pack(pady=10)

root.mainloop()