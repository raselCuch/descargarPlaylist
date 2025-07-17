import tkinter as tk
from tkinter import filedialog, messagebox
from pytube import YouTube
import os

def mostrar_interfaz_video(ventana):
    ventana.title("Descargar video de YouTube")
    ventana.geometry("400x300")
    ventana.resizable(False, False)

    def descargar_video():
        url = entrada_url.get()
        if not url:
            messagebox.showerror("Error", "Por favor ingresa un enlace de YouTube.")
            return

        carpeta_destino = filedialog.askdirectory(title="Selecciona carpeta de destino")
        if not carpeta_destino:
            return

        try:
            yt = YouTube(url)
            video = yt.streams.get_highest_resolution()
            video.download(output_path=carpeta_destino)
            messagebox.showinfo("Éxito", f"Video descargado en:\n{carpeta_destino}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo descargar el video.\n{str(e)}")

    tk.Label(ventana, text="Ingresa el enlace del video", font=("Helvetica", 12)).pack(pady=20)
    entrada_url = tk.Entry(ventana, width=50)
    entrada_url.pack(pady=10)

    tk.Button(ventana, text="Descargar", command=descargar_video, font=("Helvetica", 12)).pack(pady=20)
