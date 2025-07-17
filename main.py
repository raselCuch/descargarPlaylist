import tkinter as tk
from tkinter import messagebox
from gui.video_gui import mostrar_interfaz_video
from gui.playlist_gui import mostrar_interfaz_playlist

def main():
    root = tk.Tk()
    root.title("Descargador de YouTube")
    root.geometry("400x250")
    root.resizable(False, False)

    tk.Label(root, text="Selecciona una opción", font=("Helvetica", 16)).pack(pady=20)

    tk.Button(root, text="📥 Descargar un video", font=("Helvetica", 12), width=30, command=lambda: abrir_ventana(root, mostrar_interfaz_video)).pack(pady=10)
    tk.Button(root, text="📚 Descargar una playlist", font=("Helvetica", 12), width=30, command=lambda: abrir_ventana(root, mostrar_interfaz_playlist)).pack(pady=10)

    root.mainloop()

def abrir_ventana(ventana_anterior, funcion_interfaz):
    ventana_anterior.withdraw()  # Oculta el menú principal
    nueva_ventana = tk.Toplevel()
    funcion_interfaz(nueva_ventana)  # Llama a la función del módulo correspondiente
    nueva_ventana.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana(ventana_anterior, nueva_ventana))

def cerrar_ventana(ventana_anterior, ventana_actual):
    ventana_actual.destroy()
    ventana_anterior.deiconify()  # Vuelve a mostrar el menú principal

if __name__ == "__main__":
    main()
