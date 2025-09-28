# 🎥 YouTube Downloader

Un descargador robusto de YouTube que maneja errores 403/400 y descarga videos en MP4 y audio en MP3 con múltiples estrategias de fallback.

## ✨ Características

- **Descarga Robusta**: Maneja errores 403/400 de YouTube con múltiples estrategias
- **Formatos Optimizados**: Video en MP4 y audio en MP3
- **Múltiples Estrategias**: Fallback automático si una estrategia falla
- **Reintentos Inteligentes**: Hasta 10 reintentos con pausas progresivas
- **Anti-Detección**: Headers realistas y pausas aleatorias
- **Información del Video**: Muestra título y duración antes de descargar

## 🚀 Instalación Rápida

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/yt-downloader.git
cd yt-downloader
```

### 2. Instalación automática
```bash
chmod +x install.sh
./install.sh
```

### 3. Instalación manual
```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Instalar FFmpeg (requerido)
# macOS:
brew install ffmpeg

# Ubuntu/Debian:
sudo apt update && sudo apt install ffmpeg

# Windows:
# Descargar desde https://ffmpeg.org/download.html
```

## 📖 Uso

### Comando Básico
```bash
python main.py "URL_DEL_VIDEO" [video|audio|both]
```

### Ejemplos
```bash
# Descargar solo audio (MP3)
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" audio

# Descargar solo video (MP4)
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" video

# Descargar ambos
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" both
```

### Modo Interactivo
```bash
python main.py
# Te mostrará las opciones de uso
```

## 🔧 Solución de Problemas

### Error: "ffmpeg not found"
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Verificar instalación
ffmpeg -version
```

### Error: "HTTP Error 403: Forbidden"
- ✅ **Solucionado automáticamente**: El script usa múltiples estrategias
- Si persiste, espera unos minutos antes de intentar de nuevo

### Error: "No module named 'yt_dlp'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Videos muy largos o con restricciones
- El script automáticamente reduce la calidad si es necesario
- Usa estrategias de fallback para videos problemáticos

## 📁 Estructura del Proyecto

```
yt-downloader/
├── main.py              # Script principal (descargador robusto)
├── requirements.txt     # Dependencias de Python
├── install.sh          # Script de instalación automática
├── README.md           # Este archivo
├── .gitignore          # Archivos ignorados por Git
└── downloads/          # Directorio de descargas (se crea automáticamente)
```

## 🛠️ Características Técnicas

### Estrategias de Descarga
1. **Alta Calidad**: Mejor formato disponible
2. **Calidad Media**: 720p o menor si falla la alta
3. **Calidad Baja**: 480p o menor como último recurso
4. **Mínima**: 360p para videos muy problemáticos

### Headers Anti-Detección
- User-Agent moderno de Chrome
- Headers HTTP completos
- Pausas aleatorias entre intentos

### Manejo de Errores
- **403 Forbidden**: Reintenta con diferentes estrategias
- **400 Bad Request**: Cambia headers y formato
- **Timeout**: Pausa y reintenta
- **Formato no disponible**: Prueba formatos alternativos

## 📊 Formatos Soportados

### Video
- **MP4**: Formato principal (hasta 1080p)
- **Fallback**: WebM, AVI si MP4 no está disponible

### Audio
- **MP3**: Formato principal (hasta 320kbps)
- **Fallback**: M4A, AAC si MP3 no está disponible

## 🔒 Consideraciones Legales

- **Uso Responsable**: Solo descarga contenido que tengas derecho a descargar
- **Términos de Servicio**: Respeta los términos de YouTube
- **Derechos de Autor**: No descargues contenido protegido sin autorización

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Changelog

### v1.0.0
- ✅ Descargador robusto con múltiples estrategias
- ✅ Manejo avanzado de errores 403/400
- ✅ Soporte para MP4 y MP3
- ✅ Anti-detección con headers realistas
- ✅ Reintentos automáticos
- ✅ Información del video antes de descargar

## 📞 Soporte

Si encuentras problemas:

1. **Verifica FFmpeg**: `ffmpeg -version`
2. **Actualiza yt-dlp**: `pip install --upgrade yt-dlp`
3. **Revisa la URL**: Asegúrate de que el video sea público
4. **Espera**: Algunos videos pueden tener restricciones temporales

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

---

**¡Disfruta descargando videos de YouTube de forma robusta y confiable!** 🎉