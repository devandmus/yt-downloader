#!/usr/bin/env python3
"""
YouTube Downloader - Descargador robusto de YouTube
Descarga videos en MP4 y audio en MP3 con manejo avanzado de errores
"""

import os
import sys
import yt_dlp
from pathlib import Path
import time
import random

def create_robust_opts(output_dir, format_selector):
    """Crea opciones robustas para yt-dlp"""
    return {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': format_selector,
        'extractor_retries': 5,
        'retries': 10,
        'fragment_retries': 10,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            'Keep-Alive': '115',
            'Connection': 'keep-alive',
        },
        'sleep_interval': 2,
        'max_sleep_interval': 10,
        'sleep_interval_subtitles': 5,
        'writeinfojson': False,
        'writethumbnail': False,
        'writesubtitles': False,
        'writeautomaticsub': False,
        'ignoreerrors': False,
        'no_warnings': False,
    }

def download_with_fallback(url, output_dir, is_audio=False):
    """Descarga con múltiples estrategias de fallback"""
    
    # Estrategias de formato en orden de preferencia
    if is_audio:
        strategies = [
            'bestaudio[ext=m4a]/bestaudio/best[height<=720]',
            'bestaudio/best[height<=480]',
            'worst[height<=360]'
        ]
        file_type = "audio"
        emoji = "🎵"
    else:
        strategies = [
            'best[ext=mp4][height<=1080]/best[ext=mp4]/mp4',
            'best[height<=720]/mp4',
            'best[height<=480]',
            'worst[height<=360]'
        ]
        file_type = "video"
        emoji = "📹"
    
    for i, format_strategy in enumerate(strategies):
        try:
            print(f"{emoji} Intentando estrategia {i+1} para {file_type}...")
            
            ydl_opts = create_robust_opts(output_dir, format_strategy)
            
            if is_audio:
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',  # Calidad más baja para evitar errores
                }]
            
            # Pausa aleatoria para evitar detección
            time.sleep(random.uniform(1, 3))
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            print(f"✅ {file_type.capitalize()} descargado exitosamente con estrategia {i+1}")
            return True
            
        except Exception as e:
            print(f"❌ Estrategia {i+1} falló: {str(e)[:100]}...")
            if i < len(strategies) - 1:
                wait_time = (i + 1) * 5
                print(f"⏳ Esperando {wait_time} segundos antes del siguiente intento...")
                time.sleep(wait_time)
            continue
    
    print(f"❌ Todas las estrategias fallaron para {file_type}")
    return False

def get_video_info_safe(url):
    """Obtiene información del video de forma segura"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        print(f"⚠️ No se pudo obtener información del video: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("🎥 YouTube Downloader")
        print("=" * 30)
        print("Uso: python main.py 'URL' [video|audio|both]")
        print("\nEjemplos:")
        print("  python main.py 'https://youtube.com/watch?v=VIDEO_ID' video")
        print("  python main.py 'https://youtube.com/watch?v=VIDEO_ID' audio") 
        print("  python main.py 'https://youtube.com/watch?v=VIDEO_ID' both")
        print("\n🔧 Características:")
        print("  - Múltiples estrategias de descarga")
        print("  - Reintentos automáticos")
        print("  - Manejo robusto de errores 403/400")
        print("  - Pausas aleatorias para evitar detección")
        return
    
    url = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "both"
    
    # Crear directorio de descargas
    output_dir = "downloads"
    Path(output_dir).mkdir(exist_ok=True)
    print(f"📁 Descargando en: {os.path.abspath(output_dir)}")
    
    # Obtener información del video
    print("\n🔍 Obteniendo información del video...")
    info = get_video_info_safe(url)
    if info:
        title = info.get('title', 'Sin título')
        duration = info.get('duration', 0)
        print(f"📹 Título: {title}")
        if duration:
            minutes = duration // 60
            seconds = duration % 60
            print(f"⏱️ Duración: {minutes}:{seconds:02d}")
    
    print(f"\n🚀 Iniciando descarga en modo: {mode}")
    success = True
    
    if mode == "video":
        success = download_with_fallback(url, output_dir, is_audio=False)
    elif mode == "audio":
        success = download_with_fallback(url, output_dir, is_audio=True)
    elif mode == "both":
        print("📹 Descargando video...")
        video_success = download_with_fallback(url, output_dir, is_audio=False)
        print("\n🎵 Descargando audio...")
        audio_success = download_with_fallback(url, output_dir, is_audio=True)
        success = video_success or audio_success  # Al menos uno debe funcionar
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
                if file.is_file():
                    size = file.stat().st_size / (1024*1024)  # MB
                    print(f"  - {file.name} ({size:.1f} MB)")
    else:
        print("\n❌ No se pudo completar la descarga")
        print("💡 Sugerencias:")
        print("  - Verifica que la URL sea correcta y el video esté disponible")
        print("  - Intenta con un video diferente")
        print("  - Espera unos minutos antes de intentar de nuevo")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Descarga cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
