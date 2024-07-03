import tkinter as tk
from tkinter import ttk, filedialog, messagebox, PhotoImage
import threading
import asyncio
from model_loader import load_model
from video_processor import process_video
from image_processor import process_images
import telegram_bot

model = load_model("best.pt")  # Asumimos que el modelo se carga aquí correctamente


def start_bot_thread(root):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(telegram_bot.main())
    except Exception as e:
        messagebox.showerror("Error", str(e), parent=root)


def select_video(root):
    video_path = filedialog.askopenfilename(
        initialdir=".",
        title="Seleccionar Video",
        filetypes=[("Video files", "*.mp4;*.avi;*.mov")],
        parent=root
    )
    if video_path:
        process_video(video_path, model)


def select_directory(root):
    directory_path = filedialog.askdirectory(
        initialdir=".",
        title="Seleccionar Directorio de Imágenes",
        parent=root
    )
    if directory_path:
        process_images(directory_path, model)



def create_main_window():
    root = tk.Tk()
    root.title("Detección de Objetos con YOLO y Telegram")
    root.minsize(500, 300)

    # Cargar y colocar la imagen de fondo
    background_image = PhotoImage(file='Vaca.png')  # Asegúrate de poner la ruta correcta a tu imagen
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Configurar estilo
    style = ttk.Style(root)
    style.theme_use('clam')  # Puedes elegir entre 'alt', 'default', 'classic', 'vista', etc.

    # Menú
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Salir", command=lambda: root.quit())
    menubar.add_cascade(label="Archivo", menu=filemenu)
    root.config(menu=menubar)

    # Frame para centrar los botones
    frame = ttk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor='center')  # Centrar el frame

    # Widgets en el frame
    btn_video = ttk.Button(frame, text="Seleccionar Video", command=lambda: select_video(root))
    btn_video.pack(pady=10, fill='x')

    btn_images = ttk.Button(frame, text="Seleccionar Directorio de Imágenes", command=lambda: select_directory(root))
    btn_images.pack(pady=10, fill='x')

    btn_telegram = ttk.Button(frame, text="Iniciar Detección con Telegram",
                              command=lambda: threading.Thread(target=lambda: start_bot_thread(root)).start())
    btn_telegram.pack(pady=10, fill='x')

    # Mantener la referencia a la imagen de fondo
    root.background_image = background_image

    return root


if __name__ == "__main__":
    main_window = create_main_window()
    main_window.mainloop()