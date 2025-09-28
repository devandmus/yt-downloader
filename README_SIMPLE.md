# 🎥 YouTube Downloader - Versión Simple

Un descargador de YouTube simple y directo que funciona por consola.

## 🚀 Uso Rápido

### Opción 1: Modo Interactivo
```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar descargador interactivo
python downloader.py
```

### Opción 2: Modo Rápido (Recomendado)
```bash
# Activar entorno virtual
source venv/bin/activate

# Descargar video
python quick_download.py "https://youtube.com/watch?v=VIDEO_ID" video

# Descargar audio
python quick_download.py "https://youtube.com/watch?v=VIDEO_ID" audio

# Descargar ambos
python quick_download.py "https://youtube.com/watch?v=VIDEO_ID" both
```

## 📁 Estructura

```
yt-downloader/
├── venv/                    # Entorno virtual
├── downloads/               # Archivos descargados (se crea automáticamente)
├── downloader.py         # Versión interactiva
├── quick_download.py       # Versión rápida (recomendada)
├── requirements.txt        # Dependencias
└── README_SIMPLE.md        # Esta guía
```

## ✨ Características

- **📹 Video**: Mejor calidad hasta 1080p
- **🎵 Audio**: MP3 de alta calidad
- **📁 Descarga Local**: Archivos se guardan en `downloads/`
- **🚀 Rápido**: Sin interfaz gráfica, solo consola
- **✅ Simple**: Fácil de usar

## 🎯 Ejemplos de Uso

```bash
# Descargar video de un tutorial
python quick_download.py "https://youtube.com/watch?v=dQw4w9WgXcQ" video

# Descargar audio de una canción
python quick_download.py "https://youtube.com/watch?v=dQw4w9WgXcQ" audio

# Descargar video y audio
python quick_download.py "https://youtube.com/watch?v=dQw4w9WgXcQ" both
```

## 📋 Requisitos

- Python 3.7+
- Entorno virtual activado
- Dependencias instaladas (`pip install -r requirements.txt`)

## 🔧 Solución de Problemas

Si hay errores de SSL:
```bash
# Actualizar yt-dlp
pip install --upgrade yt-dlp
```

Si no funciona la descarga:
```bash
# Verificar que la URL sea de YouTube
# Probar con un video más corto primero
```

## 📄 Archivos Generados

Los archivos se guardan en la carpeta `downloads/` con nombres descriptivos:
- `Nombre del Video.mp4` (video)
- `Nombre del Video.mp3` (audio)

¡Listo para usar! 🎉
