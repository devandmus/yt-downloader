#!/usr/bin/env python3
"""
YouTube Downloader - Versión Consola Simple
Descarga videos y audio de YouTube en la mejor calidad
"""

import os
import yt_dlp
from pathlib import Path
import sys

def download_video(url, output_dir="downloads"):
    """Descarga video en formato MP4"""
    print("📹 Descargando video en MP4...")
    
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'best[ext=mp4][height<=1080]/best[ext=mp4]/best',
        'merge_output_format': 'mp4',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("✅ Video descargado exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error descargando video: {e}")
        return False

def download_audio(url, output_dir="downloads"):
    """Descarga audio en formato MP3"""
    print("🎵 Descargando audio en MP3...")
    
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("✅ Audio descargado exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error descargando audio: {e}")
        return False

def get_video_info(url):
    """Obtiene información del video"""
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        print(f"❌ Error obteniendo información: {e}")
        return None

def main():
    print("🎥 YouTube Downloader - Consola")
    print("=" * 40)
    
    # Obtener URL
    url = input("\n📎 Ingresa la URL del video de YouTube: ").strip()
    if not url:
        print("❌ URL no válida")
        return
    
    # Crear directorio de descargas
    output_dir = "downloads"
    Path(output_dir).mkdir(exist_ok=True)
    print(f"📁 Los archivos se guardarán en: {os.path.abspath(output_dir)}")
    
    # Obtener información del video
    print("\n🔍 Obteniendo información del video...")
    info = get_video_info(url)
    if info:
        title = info.get('title', 'Sin título')
        duration = info.get('duration', 0)
        print(f"📹 Título: {title}")
        print(f"⏱️ Duración: {duration} segundos")
    
    # Opciones de descarga
    print("\n¿Qué quieres descargar?")
    print("1. Solo video")
    print("2. Solo audio") 
    print("3. Video y audio")
    
    choice = input("\nSelecciona una opción (1-3): ").strip()
    
    success = True
    
    if choice == "1":
        success = download_video(url, output_dir)
    elif choice == "2":
        success = download_audio(url, output_dir)
    elif choice == "3":
        print("\n🚀 Descargando video y audio...")
        video_success = download_video(url, output_dir)
        audio_success = download_audio(url, output_dir)
        success = video_success and audio_success
    else:
        print("❌ Opción no válida")
        return
    
    if success:
        print(f"\n🎉 ¡Descarga completada!")
        print(f"📁 Archivos guardados en: {os.path.abspath(output_dir)}")
        
        # Mostrar archivos descargados
        files = list(Path(output_dir).glob("*"))
        if files:
            print("\n📄 Archivos descargados:")
            for file in files:
                print(f"  - {file.name}")
    else:
        print("\n❌ Hubo errores durante la descarga")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Descarga cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
