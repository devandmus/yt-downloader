#!/usr/bin/env python3
"""
YouTube Downloader - Descargador robusto de YouTube con interfaz interactiva
Descarga videos en MP4 y audio en MP3 con streaming de progreso en tiempo real
"""

import os
import sys
import yt_dlp
from pathlib import Path
import time
import random
from datetime import datetime

def progress_hook(d):
    """Hook para mostrar progreso en tiempo real con streaming"""
    if d['status'] == 'downloading':
        # Calcular progreso
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
        speed = d.get('speed', 0)
        eta = d.get('eta', 0)
        
        if total > 0:
            percent = (downloaded / total) * 100
            downloaded_mb = downloaded / (1024 * 1024)
            total_mb = total / (1024 * 1024)
            speed_mb = (speed / (1024 * 1024)) if speed else 0
            
            # Crear barra de progreso
            bar_length = 30
            filled = int(bar_length * downloaded / total)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            # Formatear tiempo estimado
            eta_str = f"{eta}s" if eta else "calculando..."
            
            # Imprimir progreso (con \r para sobrescribir línea)
            print(f"\r🔄 [{bar}] {percent:.1f}% | {downloaded_mb:.1f}/{total_mb:.1f} MB | ⚡ {speed_mb:.2f} MB/s | ETA: {eta_str}", end='', flush=True)
    
    elif d['status'] == 'finished':
        print("\n✅ Descarga completada, procesando...", flush=True)
    
    elif d['status'] == 'error':
        print("\n❌ Error durante la descarga", flush=True)

def create_robust_opts(output_dir, format_selector, show_progress=True):
    """Crea opciones robustas para yt-dlp"""
    # Sanitizar el nombre del archivo para evitar caracteres problemáticos
    safe_outtmpl = os.path.join(output_dir, '%(title)s.%(ext)s')
    
    opts = {
        'outtmpl': safe_outtmpl,
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
        'noplaylist': True,  # Solo descargar el video, no la playlist completa
    }
    
    # Añadir hook de progreso para streaming en tiempo real
    if show_progress:
        opts['progress_hooks'] = [progress_hook]
    
    return opts

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
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"\n{emoji} [{timestamp}] Intentando estrategia {i+1} para {file_type}...")
            print("📊 Iniciando streaming de progreso...\n")
            
            ydl_opts = create_robust_opts(output_dir, format_strategy, show_progress=True)
            
            if is_audio:
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            
            # Pausa aleatoria para evitar detección
            time.sleep(random.uniform(1, 3))
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            print(f"\n✅ {file_type.capitalize()} descargado exitosamente con estrategia {i+1}")
            return True
            
        except Exception as e:
            print(f"\n❌ Estrategia {i+1} falló: {str(e)[:100]}...")
            if i < len(strategies) - 1:
                wait_time = (i + 1) * 5
                print(f"⏳ Esperando {wait_time} segundos antes del siguiente intento...")
                time.sleep(wait_time)
            continue
    
    print(f"\n❌ Todas las estrategias fallaron para {file_type}")
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
        print(f"⚠️  No se pudo obtener información del video: {e}")
        return None

def print_banner():
    """Imprime el banner de bienvenida"""
    print("\n" + "="*60)
    print("🎥  YOUTUBE DOWNLOADER - Modo Interactivo")
    print("="*60)
    print("📹  Descarga videos en MP4 o audio en MP3")
    print("⚡  Streaming de progreso en tiempo real")
    print("🔄  Múltiples estrategias de fallback")
    print("="*60 + "\n")

def print_menu():
    """Imprime el menú de opciones"""
    print("\n" + "-"*60)
    print("🎯  OPCIONES:")
    print("-"*60)
    print("  [1] Descargar VIDEO (MP4)")
    print("  [2] Descargar AUDIO (MP3)")
    print("  [3] Descargar AMBOS (Video + Audio)")
    print("  [4] Salir")
    print("-"*60)

def interactive_mode():
    """Modo interactivo - UI por consola"""
    output_dir = "/downloads"
    # Asegurar que el directorio existe y tiene permisos correctos
    download_path = Path(output_dir)
    download_path.mkdir(parents=True, exist_ok=True)
    try:
        # Verificar permisos de escritura
        test_file = download_path / ".test_write"
        test_file.touch()
        test_file.unlink()
    except (PermissionError, OSError) as e:
        print(f"⚠️  Advertencia: No se pueden escribir archivos en {output_dir}: {e}")
        print("💡 Verifica los permisos del volumen montado")
    
    print_banner()
    print(f"📁 Carpeta de descargas: {output_dir}")
    
    while True:
        try:
            print_menu()
            choice = input("\n👉 Selecciona una opción [1-4]: ").strip()
            
            if choice == '4':
                print("\n👋 ¡Hasta luego! Gracias por usar YouTube Downloader\n")
                break
            
            if choice not in ['1', '2', '3']:
                print("\n❌ Opción no válida. Elige 1, 2, 3 o 4")
                continue
            
            # Pedir URL
            print("\n" + "="*60)
            url = input("🔗 Ingresa la URL del video de YouTube: ").strip()
            
            if not url:
                print("❌ URL vacía. Intenta de nuevo.")
                continue
            
            # Validar que sea una URL
            if not url.startswith('http'):
                print("❌ URL no válida. Debe comenzar con http:// o https://")
                continue
            
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
                    print(f"⏱️  Duración: {minutes}:{seconds:02d}")
            
            # Procesar según la opción
            success = False
            
            if choice == '1':
                print("\n🚀 Iniciando descarga de VIDEO...")
                success = download_with_fallback(url, output_dir, is_audio=False)
            
            elif choice == '2':
                print("\n🚀 Iniciando descarga de AUDIO...")
                success = download_with_fallback(url, output_dir, is_audio=True)
            
            elif choice == '3':
                print("\n🚀 Iniciando descarga de VIDEO y AUDIO...")
                print("\n📹 Descargando video...")
                video_success = download_with_fallback(url, output_dir, is_audio=False)
                print("\n🎵 Descargando audio...")
                audio_success = download_with_fallback(url, output_dir, is_audio=True)
                success = video_success or audio_success
            
            # Mostrar resultado
            if success:
                print("\n" + "="*60)
                print("🎉 ¡DESCARGA COMPLETADA!")
                print("="*60)
                print(f"📁 Archivos guardados en: {output_dir}")
                
                # Mostrar archivos descargados
                files = list(Path(output_dir).glob("*"))
                if files:
                    print("\n📄 Archivos en carpeta de descargas:")
                    for file in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
                        if file.is_file():
                            size = file.stat().st_size / (1024*1024)
                            print(f"  - {file.name} ({size:.1f} MB)")
                print("="*60)
            else:
                print("\n" + "="*60)
                print("❌ NO SE PUDO COMPLETAR LA DESCARGA")
                print("="*60)
                print("💡 Sugerencias:")
                print("  - Verifica que la URL sea correcta")
                print("  - Asegúrate de que el video esté disponible")
                print("  - Intenta con un video diferente")
                print("  - Espera unos minutos antes de reintentar")
                print("="*60)
            
            # Preguntar si quiere continuar
            print("\n")
            continuar = input("❓ ¿Descargar otro video? (s/n): ").strip().lower()
            if continuar != 's' and continuar != 'si' and continuar != 'y' and continuar != 'yes':
                print("\n👋 ¡Hasta luego!\n")
                break
        
        except KeyboardInterrupt:
            print("\n\n👋 Descarga cancelada. ¡Hasta luego!\n")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            print("Volviendo al menú principal...\n")

def main():
    """Punto de entrada principal"""
    # Si se pasan argumentos, usar modo comando (backward compatibility)
    if len(sys.argv) > 1:
        url = sys.argv[1]
        mode = sys.argv[2] if len(sys.argv) > 2 else "both"
        
        output_dir = "/downloads"
        download_path = Path(output_dir)
        download_path.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Descargando en: {output_dir}")
        print(f"🚀 Modo: {mode}\n")
        
        success = False
        if mode == "video":
            success = download_with_fallback(url, output_dir, is_audio=False)
        elif mode == "audio":
            success = download_with_fallback(url, output_dir, is_audio=True)
        elif mode == "both":
            video_success = download_with_fallback(url, output_dir, is_audio=False)
            audio_success = download_with_fallback(url, output_dir, is_audio=True)
            success = video_success or audio_success
        
        sys.exit(0 if success else 1)
    else:
        # Modo interactivo (por defecto)
        interactive_mode()

if __name__ == "__main__":
    main()
