#!/usr/bin/env python3
"""
YouTube Downloader - Versión Mejorada
Descarga videos en MP4 y audio en MP3
"""

import os
import sys
import yt_dlp
from pathlib import Path

def download_video(url, output_dir="downloads"):
    """Descarga video en formato MP4"""
    print("📹 Descargando video en MP4...")
    
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'best[ext=mp4]/best[height<=1080]/best',
        'merge_output_format': 'mp4',
        'writethumbnail': False,
        'writeinfojson': False,
        'writesubtitles': False,
        'writeautomaticsub': False,
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
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'writethumbnail': False,
        'writeinfojson': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("✅ Audio descargado exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error descargando audio: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("🎥 YouTube Downloader - Versión Mejorada")
        print("=" * 45)
        print("Uso: python downloader_fixed.py 'URL' [video|audio|both]")
        print("\nEjemplos:")
        print("  python downloader_fixed.py 'https://youtube.com/watch?v=VIDEO_ID' video")
        print("  python downloader_fixed.py 'https://youtube.com/watch?v=VIDEO_ID' audio")
        print("  python downloader_fixed.py 'https://youtube.com/watch?v=VIDEO_ID' both")
        return
    
    url = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "both"
    
    # Crear directorio de descargas
    output_dir = "downloads"
    Path(output_dir).mkdir(exist_ok=True)
    print(f"📁 Descargando en: {os.path.abspath(output_dir)}")
    
    success = True
    
    if mode == "video":
        success = download_video(url, output_dir)
    elif mode == "audio":
        success = download_audio(url, output_dir)
    elif mode == "both":
        print("🚀 Descargando video y audio...")
        video_success = download_video(url, output_dir)
        audio_success = download_audio(url, output_dir)
        success = video_success and audio_success
    else:
        print("❌ Modo no válido. Usa: video, audio, o both")
        return
    
    if success:
        print(f"\n🎉 ¡Descarga completada!")
        print(f"📁 Archivos en: {os.path.abspath(output_dir)}")
        
        # Mostrar archivos
        files = list(Path(output_dir).glob("*"))
        if files:
            print("\n📄 Archivos descargados:")
            for file in files:
                size = file.stat().st_size / (1024*1024)  # MB
                print(f"  - {file.name} ({size:.1f} MB)")
    else:
        print("\n❌ Hubo errores durante la descarga")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Descarga cancelada")
    except Exception as e:
        print(f"\n❌ Error: {e}")
