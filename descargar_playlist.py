import os
import yt_dlp
import eyed3
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from glob import glob

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        carpeta_descarga.set(carpeta)

def log(texto):
    text_output.insert(tk.END, texto + "\n")
    text_output.see(tk.END)
    root.update()

def descargar_playlist():
    url = entry_url.get().strip()
    carpeta = carpeta_descarga.get().strip()

    if not url or not carpeta:
        messagebox.showerror("Error", "Debes ingresar un enlace y seleccionar carpeta.")
        return

    text_output.delete('1.0', tk.END)
    log("🎵 Iniciando descarga video por video...\n")
    os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"
    descargados = 0
    errores = 0

    # Extraer metadata de la playlist
    ydl_info_opts = {
        'quiet': True,
        'extract_flat': True,
        'nocache': True,
        'cachedir': False,
        'ignoreerrors': True
    }
    with yt_dlp.YoutubeDL(ydl_info_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            entries = [e for e in info.get('entries', []) if e]
            total = len(entries)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener la lista de videos:\n{e}")
            return

    log(f"📃 Playlist detectada con {total} videos\n")

    # Descargar uno por uno
    for i, entry in enumerate(entries, start=1):
        try:
            video_url = entry.get("webpage_url") or entry.get("url")
            title = entry.get("title", f"video_{i}")
            if not video_url:
                raise ValueError("URL no disponible para este video.")
            log(f"🎧 [{i}/{total}] Descargando: {title}...")
        except Exception as e:
            errores += 1
            log(f"❌ [{i}/{total}] Error al obtener información del video: {e}")
            continue

        if not video_url:
            errores += 1
            log(f"❌ [{i}/{total}] Error: URL no disponible para este video.")
            continue

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(carpeta, '%(title)s.%(ext)s'),
            'nocache': True,
            'cachedir': False,
            'ignoreerrors': True,
            'quiet': True,
            'writethumbnail': True,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                },
                {
                    'key': 'FFmpegMetadata',
                },
            ],
            'ffmpeg_location': r"C:\ffmpeg\bin\ffmpeg.exe"
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(video_url, download=True)
                if result is None:
                    raise Exception("No se pudo extraer información del video.")

                filename = ydl.prepare_filename(result)
                mp3_path = os.path.splitext(filename)[0] + ".mp3"
                webp_path = os.path.splitext(filename)[0] + ".webp"

                if os.path.exists(webp_path) and os.path.exists(mp3_path):
                    audiofile = eyed3.load(mp3_path)
                    if audiofile.tag is None:
                        audiofile.initTag()
                    with open(webp_path, "rb") as img:
                        audiofile.tag.images.set(3, img.read(), "image/webp", u"Portada")
                        audiofile.tag.save()
                    os.remove(webp_path)
                    descargados += 1
                    log(f"✔️ [{i}/{total}] {os.path.basename(mp3_path)} (✅ Miniatura incluida)")
                else:
                    errores += 1
                    log(f"⚠️ [{i}/{total}] {title}: Miniatura o archivo mp3 no encontrados")

        except Exception as e:
            errores += 1
            log(f"❌ [{i}/{total}] Error: {e}")

    # Limpiar miniatura de la playlist (jpg)
    for img in glob(os.path.join(carpeta, "*.jpg")):
        try:
            os.remove(img)
            log(f"🗑️ Miniatura de playlist eliminada: {os.path.basename(img)}")
        except Exception as e:
            log(f"⚠️ No se pudo eliminar {img}: {e}")

    # Final
    log("\n🎉 Proceso finalizado")
    log(f"✅ Canciones procesadas correctamente: {descargados}")
    log(f"❌ Errores o sin miniatura: {errores}")

# Interfaz gráfica
root = tk.Tk()
root.title("Descargador de Playlist YouTube")
root.geometry("750x550")

tk.Label(root, text="🔗 URL de la playlist:").pack(anchor="w", padx=10, pady=5)
entry_url = tk.Entry(root, width=90)
entry_url.pack(padx=10)

tk.Label(root, text="📁 Carpeta de descarga:").pack(anchor="w", padx=10, pady=5)
frame_carpeta = tk.Frame(root)
frame_carpeta.pack(padx=10)
carpeta_descarga = tk.StringVar()
entry_carpeta = tk.Entry(frame_carpeta, width=65, textvariable=carpeta_descarga)
entry_carpeta.pack(side=tk.LEFT)
tk.Button(frame_carpeta, text="Seleccionar...", command=seleccionar_carpeta).pack(side=tk.LEFT, padx=5)

tk.Button(root, text="⬇️ Descargar Playlist", command=descargar_playlist, bg="#4CAF50", fg="white").pack(pady=10)

text_output = scrolledtext.ScrolledText(root, height=20)
text_output.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
