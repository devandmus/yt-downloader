#!/usr/bin/env python3
"""
YouTube Downloader - Versión Simplificada para macOS
Descarga videos y audio de YouTube en la mejor calidad
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
import yt_dlp
from pathlib import Path
import re
import sys

# Configuración para macOS
if sys.platform == "darwin":
    import warnings
    warnings.filterwarnings("ignore")

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("600x500")
        
        # Variables
        self.download_path = tk.StringVar(value=str(Path.home() / "Downloads"))
        self.is_downloading = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(
            main_frame, 
            text="YouTube Downloader", 
            font=('Arial', 18, 'bold')
        )
        title_label.pack(pady=(0, 20))
        
        # Frame para URL
        url_frame = tk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(url_frame, text="URL del Video:", font=('Arial', 12, 'bold')).pack(anchor=tk.W)
        
        self.url_entry = tk.Entry(url_frame, font=('Arial', 11), width=60)
        self.url_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Frame para opciones
        options_frame = tk.LabelFrame(main_frame, text="Opciones de Descarga", font=('Arial', 12, 'bold'))
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.download_video = tk.BooleanVar(value=True)
        self.download_audio = tk.BooleanVar(value=True)
        
        tk.Checkbutton(
            options_frame,
            text="Descargar Video (Mejor Calidad)",
            variable=self.download_video,
            font=('Arial', 11)
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        tk.Checkbutton(
            options_frame,
            text="Descargar Audio (Mejor Calidad)",
            variable=self.download_audio,
            font=('Arial', 11)
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        # Frame para ruta
        path_frame = tk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(path_frame, text="Carpeta de Descarga:", font=('Arial', 12, 'bold')).pack(anchor=tk.W)
        
        path_input_frame = tk.Frame(path_frame)
        path_input_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.path_entry = tk.Entry(path_input_frame, textvariable=self.download_path, font=('Arial', 11))
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Button(
            path_input_frame,
            text="Seleccionar",
            command=self.browse_folder,
            font=('Arial', 10)
        ).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Botones
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.download_btn = tk.Button(
            button_frame,
            text="Descargar",
            command=self.start_download,
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            padx=20,
            pady=10
        )
        self.download_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = tk.Button(
            button_frame,
            text="Limpiar",
            command=self.clear_fields,
            font=('Arial', 12, 'bold'),
            bg='#f44336',
            fg='white',
            padx=20,
            pady=10
        )
        self.clear_btn.pack(side=tk.LEFT)
        
        # Barra de progreso
        self.progress_frame = tk.Frame(main_frame)
        self.progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.progress_var = tk.StringVar(value="Listo para descargar")
        self.progress_label = tk.Label(self.progress_frame, textvariable=self.progress_var, font=('Arial', 11))
        self.progress_label.pack(anchor=tk.W)
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))
        
        # Área de log
        log_frame = tk.LabelFrame(main_frame, text="Log de Descarga", font=('Arial', 12, 'bold'))
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_frame, height=8, font=('Consolas', 9), wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
    def browse_folder(self):
        """Permite al usuario seleccionar una carpeta de descarga"""
        folder = filedialog.askdirectory(initialdir=self.download_path.get())
        if folder:
            self.download_path.set(folder)
            
    def clear_fields(self):
        """Limpia todos los campos"""
        self.url_entry.delete(0, tk.END)
        self.log_text.delete(1.0, tk.END)
        self.progress_var.set("Listo para descargar")
        self.progress_bar.stop()
        
    def log_message(self, message):
        """Añade un mensaje al log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def is_valid_url(self, url):
        """Valida si la URL es de YouTube"""
        youtube_patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=',
            r'(?:https?://)?(?:www\.)?youtu\.be/',
            r'(?:https?://)?(?:www\.)?youtube\.com/embed/',
            r'(?:https?://)?(?:www\.)?youtube\.com/v/'
        ]
        return any(re.search(pattern, url) for pattern in youtube_patterns)
        
    def get_video_info(self, url):
        """Obtiene información del video"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            raise Exception(f"Error al obtener información del video: {str(e)}")
            
    def download_video(self, url, output_path):
        """Descarga el video en la mejor calidad"""
        ydl_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'format': 'best[height<=1080]/best',
            'progress_hooks': [self.progress_hook],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
    def download_audio(self, url, output_path):
        """Descarga el audio en la mejor calidad"""
        ydl_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'audioquality': '0',
            'progress_hooks': [self.progress_hook],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
    def progress_hook(self, d):
        """Hook para mostrar el progreso de descarga"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                self.progress_var.set(f"Descargando... {percent:.1f}%")
            else:
                self.progress_var.set("Descargando...")
        elif d['status'] == 'finished':
            self.progress_var.set("Procesando...")
            
    def start_download(self):
        """Inicia el proceso de descarga en un hilo separado"""
        if self.is_downloading:
            messagebox.showwarning("Advertencia", "Ya hay una descarga en progreso")
            return
            
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Por favor ingresa una URL de YouTube")
            return
            
        if not self.is_valid_url(url):
            messagebox.showerror("Error", "Por favor ingresa una URL válida de YouTube")
            return
            
        if not (self.download_video.get() or self.download_audio.get()):
            messagebox.showerror("Error", "Selecciona al menos una opción de descarga")
            return
            
        # Crear carpeta de descarga si no existe
        output_path = Path(self.download_path.get())
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Iniciar descarga en hilo separado
        self.is_downloading = True
        self.download_btn.config(state='disabled')
        self.progress_bar.start()
        
        thread = threading.Thread(target=self.download_thread, args=(url, str(output_path)))
        thread.daemon = True
        thread.start()
        
    def download_thread(self, url, output_path):
        """Hilo para la descarga"""
        try:
            self.log_message("Obteniendo información del video...")
            video_info = self.get_video_info(url)
            title = video_info.get('title', 'Video sin título')
            self.log_message(f"Título: {title}")
            self.log_message(f"Duración: {video_info.get('duration', 'Desconocida')} segundos")
            
            if self.download_video.get():
                self.log_message("Iniciando descarga de video...")
                self.download_video(url, output_path)
                self.log_message("Video descargado exitosamente")
                
            if self.download_audio.get():
                self.log_message("Iniciando descarga de audio...")
                self.download_audio(url, output_path)
                self.log_message("Audio descargado exitosamente")
                
            self.log_message(f"¡Descarga completada! Archivos guardados en: {output_path}")
            self.progress_var.set("Descarga completada")
            
        except Exception as e:
            error_msg = f"Error durante la descarga: {str(e)}"
            self.log_message(error_msg)
            self.progress_var.set("Error en la descarga")
            messagebox.showerror("Error", error_msg)
            
        finally:
            self.is_downloading = False
            self.download_btn.config(state='normal')
            self.progress_bar.stop()

def main():
    """Función principal"""
    try:
        root = tk.Tk()
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        app = YouTubeDownloader(root)
        
        # Centrar ventana
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        root.geometry(f"+{x}+{y}")
        
        root.mainloop()
        
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        print("Intentando con configuración alternativa...")
        
        # Versión de consola como fallback
        console_downloader()

def console_downloader():
    """Versión de consola como fallback"""
    print("\n=== YouTube Downloader (Modo Consola) ===")
    print("Si la interfaz gráfica no funciona, usa esta versión de consola\n")
    
    url = input("Ingresa la URL del video de YouTube: ").strip()
    if not url:
        print("URL no válida")
        return
        
    download_path = input(f"Carpeta de descarga (Enter para ~/Downloads): ").strip()
    if not download_path:
        download_path = str(Path.home() / "Downloads")
    
    print("\n¿Qué quieres descargar?")
    print("1. Solo video")
    print("2. Solo audio")
    print("3. Video y audio")
    
    choice = input("Selecciona (1-3): ").strip()
    
    try:
        output_path = Path(download_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        if choice in ['1', '3']:
            print("Descargando video...")
            ydl_opts = {
                'outtmpl': os.path.join(str(output_path), '%(title)s.%(ext)s'),
                'format': 'best[height<=1080]/best',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print("Video descargado!")
            
        if choice in ['2', '3']:
            print("Descargando audio...")
            ydl_opts = {
                'outtmpl': os.path.join(str(output_path), '%(title)s.%(ext)s'),
                'format': 'bestaudio/best',
                'extractaudio': True,
                'audioformat': 'mp3',
                'audioquality': '0',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print("Audio descargado!")
            
        print(f"\n¡Descarga completada! Archivos en: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
