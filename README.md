# 🎥 YouTube Downloader

Un descargador de YouTube moderno y fácil de usar que descarga videos y audio por separado en la mejor calidad posible.

## ✨ Características

- 📹 **Descarga de Video**: Obtiene el video en la mejor calidad disponible (hasta 1080p)
- 🎵 **Descarga de Audio**: Extrae el audio en la mejor calidad (formato MP3)
- 🎨 **Interfaz Moderna**: GUI intuitiva y atractiva con tema oscuro
- 📁 **Selección de Carpeta**: Elige dónde guardar tus descargas
- 📊 **Progreso en Tiempo Real**: Barra de progreso y log detallado
- ✅ **Validación de URLs**: Verifica que las URLs sean de YouTube
- 🚀 **Descarga Paralela**: Descarga video y audio simultáneamente

## 🛠️ Instalación

### Requisitos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clona o descarga el proyecto**:
   ```bash
   git clone <url-del-repositorio>
   cd yt-downloader
   ```

2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta la aplicación**:
   ```bash
   python youtube_downloader.py
   ```

## 🚀 Uso

1. **Abre la aplicación** ejecutando `python youtube_downloader.py`

2. **Pega la URL** del video de YouTube que quieres descargar

3. **Selecciona las opciones**:
   - ✅ Descargar Video (Mejor Calidad)
   - ✅ Descargar Audio (Mejor Calidad)

4. **Elige la carpeta** donde quieres guardar los archivos (por defecto: Downloads)

5. **Haz clic en "🚀 Descargar"** y espera a que termine

## 📋 Dependencias

- `yt-dlp`: Biblioteca principal para descargar de YouTube
- `tkinter`: Interfaz gráfica (incluida con Python)
- `Pillow`: Manejo de imágenes (opcional, para futuras mejoras)

## 🎯 Características Técnicas

### Calidad de Video
- **Resolución**: Hasta 1080p (Full HD)
- **Formato**: Mejor formato disponible (MP4, WebM, etc.)
- **Optimización**: Selecciona automáticamente la mejor calidad

### Calidad de Audio
- **Formato**: MP3
- **Calidad**: Mejor bitrate disponible
- **Extracción**: Audio limpio sin video

### Interfaz de Usuario
- **Tema Oscuro**: Diseño moderno y fácil para los ojos
- **Responsive**: Se adapta al tamaño de la ventana
- **Log en Tiempo Real**: Ve el progreso de la descarga
- **Validación**: Verifica URLs antes de descargar

## 🔧 Solución de Problemas

### Error: "No module named 'yt_dlp'"
```bash
pip install yt-dlp
```

### Error: "No module named 'tkinter'"
En Ubuntu/Debian:
```bash
sudo apt-get install python3-tk
```

En macOS:
```bash
brew install python-tk
```

### La descarga es muy lenta
- Verifica tu conexión a internet
- Algunos videos pueden tener restricciones de descarga
- Intenta con videos más cortos primero

## 📁 Estructura del Proyecto

```
yt-downloader/
├── youtube_downloader.py    # Aplicación principal
├── requirements.txt         # Dependencias
└── README.md               # Este archivo
```

## 🎨 Capturas de Pantalla

La aplicación incluye:
- Campo para URL de YouTube
- Opciones de descarga (video/audio)
- Selector de carpeta de destino
- Barra de progreso
- Log detallado de descarga
- Botones de acción (Descargar/Limpiar)

## ⚖️ Consideraciones Legales

- **Uso Responsable**: Solo descarga contenido que tengas derecho a descargar
- **Términos de Servicio**: Respeta los términos de servicio de YouTube
- **Derechos de Autor**: No uses contenido protegido sin autorización
- **Uso Personal**: Ideal para uso personal y educativo

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras algún error o tienes ideas para mejorar:

1. Reporta bugs o problemas
2. Sugiere nuevas características
3. Mejora la documentación
4. Optimiza el código

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🆘 Soporte

Si tienes problemas o preguntas:
1. Revisa la sección de solución de problemas
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de usar URLs válidas de YouTube
4. Revisa los logs de la aplicación para más detalles

---

**¡Disfruta descargando tus videos favoritos de YouTube! 🎉**
