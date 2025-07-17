import tkinter as tk
from tkinter import filedialog, messagebox
from pytube import Playlist
import os

def mostrar_interfaz_playlist(ventana):
    ventana.title("Descargar playlist de YouTube")
    ventana.geometry("400x350")
    ventana.resizable(False, False)

    def descargar_playlist():
        url = entrada_url.get()
        cantidad = entrada_cantidad.get()

        if not url:
            messagebox.showerror("Error", "Por favor ingresa el enlace de la playlist.")
            return
        if not cantidad.isdigit():
            messagebox.showerror("Error", "Cantidad debe ser un número.")
            return

        carpeta_destino = filedialog.askdirectory(title="Selecciona carpeta de destino")
        if not carpeta_destino:
            return

        try:
            p = Playlist(url)
            videos = p.videos[:int(cantidad)]

            for i, video in enumerate(videos):
                video.streams.get_highest_resolution().download(output_path=carpeta_destino)
            
            messagebox.showinfo("Éxito", f"{len(videos)} videos descargados en:\n{carpeta_destino}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo descargar la playlist.\n{str(e)}")

    tk.Label(ventana, text="Enlace de la playlist", font=("Helvetica", 12)).pack(pady=10)
    entrada_url = tk.Entry(ventana, width=50)
    entrada_url.pack(pady=5)

    tk.Label(ventana, text="Cantidad de videos a descargar", font=("Helvetica", 12)).pack(pady=10)
    entrada_cantidad = tk.Entry(ventana, width=10)
    entrada_cantidad.pack(pady=5)

    tk.Button(ventana, text="Descargar", command=descargar_playlist, font=("Helvetica", 12)).pack(pady=20)
