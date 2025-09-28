# 🎥 YouTube Downloader

Un descargador de YouTube moderno y completo que descarga videos y audio por separado en la mejor calidad posible.

## ✨ Características

- 📹 **Video MP4**: Descarga en la mejor calidad hasta 1080p
- 🎵 **Audio MP3**: Extrae audio en alta calidad (320 kbps)
- 🖥️ **Múltiples Interfaces**: GUI moderna, consola interactiva y modo rápido
- 🚀 **Fácil de Usar**: Scripts de instalación automática
- 🔧 **Configuración Completa**: Entorno virtual y dependencias incluidas

## 🚀 Instalación Rápida

### Opción 1: Script Automático
```bash
chmod +x install.sh
./install.sh
```

### Opción 2: Manual
```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Instalar FFmpeg (macOS)
brew install ffmpeg
```

## 📖 Uso

### Versión Rápida (Recomendada)
```bash
source venv/bin/activate
python downloader_fixed.py "https://youtube.com/watch?v=VIDEO_ID" both
```

### Versión Interactiva
```bash
source venv/bin/activate
python downloader.py
```

### Interfaz Gráfica
```bash
source venv/bin/activate
python youtube_downloader_simple.py
```

## 📁 Estructura del Proyecto

```
yt-downloader/
├── downloader_fixed.py      # Versión mejorada (recomendada)
├── downloader.py            # Versión interactiva
├── quick_download.py        # Versión rápida
├── youtube_downloader.py    # GUI completa
├── youtube_downloader_simple.py # GUI simplificada
├── requirements.txt         # Dependencias
├── install.sh             # Script de instalación
├── README.md              # Documentación completa
├── README_SIMPLE.md       # Guía simple
└── .gitignore            # Archivos ignorados
```

## 🎯 Ejemplos de Uso

```bash
# Descargar video y audio
python downloader_fixed.py "https://youtube.com/watch?v=dQw4w9WgXcQ" both

# Solo video
python downloader_fixed.py "https://youtube.com/watch?v=dQw4w9WgXcQ" video

# Solo audio
python downloader_fixed.py "https://youtube.com/watch?v=dQw4w9WgXcQ" audio
```

## 📋 Requisitos

- Python 3.7+
- FFmpeg (para conversión de audio)
- Conexión a internet

## 🔧 Solución de Problemas

### Error de SSL
```bash
pip install --upgrade yt-dlp
```

### FFmpeg no encontrado
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

## 📄 Archivos Generados

Los archivos se guardan en la carpeta `downloads/`:
- `Nombre del Video.mp4` (video)
- `Nombre del Video.mp3` (audio)

## ⚖️ Consideraciones Legales

- Solo para uso personal y educativo
- Respeta los términos de servicio de YouTube
- No uses contenido protegido sin autorización

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

---

**¡Disfruta descargando tus videos favoritos de YouTube! 🎉**
