# 🎥 YouTube Downloader

Descargador de YouTube con **interfaz interactiva** y **progreso en tiempo real**. Totalmente dockerizado.

## 🚀 Instalación

```bash
docker-compose up -d
```

## 🎯 Uso

```bash
./yt-downloader.sh
```

Este comando abre el shell interactivo. **¡Listo!** Ingresa las URLs cuando se te pida. Los archivos se guardan en `./downloads/`

## 📖 Interfaz

```
🎯  OPCIONES:
  [1] Descargar VIDEO (MP4)
  [2] Descargar AUDIO (MP3)
  [3] Descargar AMBOS (Video + Audio)
  [4] Salir
```

**Ejemplo de progreso:**
```
🔄 [████████████░░░░░░] 65.3% | 45.2/69.1 MB | ⚡ 2.34 MB/s | ETA: 12s
```

## 🛠️ Comandos Docker

```bash
# Construir y levantar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down

# Reconstruir imagen
docker-compose build --no-cache
```

## 📁 Estructura

```
yt-downloader/
├── yt-downloader.sh      # 🚀 Comando único
├── docker-compose.yml     # Configuración Docker
├── Dockerfile            # Imagen Docker
├── main.py               # Código principal
├── requirements.txt      # Dependencias
├── docs/                 # 📚 Documentación técnica
│   ├── AS_IS.md          # Estado actual del sistema (As-Is)
│   └── COMPONENTS.md     # Referencia de componentes
└── downloads/            # 📁 Archivos descargados
```

> **Tech lead:** Ver [docs/AS_IS.md](docs/AS_IS.md) para documentación completa del estado As-Is.

## 🐛 Solución de Problemas

### Docker no instalado
```bash
# macOS
brew install --cask docker

# Ubuntu/Debian
sudo apt install docker.io docker-compose
```

### Permisos
```bash
chmod +x yt-downloader.sh
```

### Archivos no aparecen
```bash
# Verificar carpeta
ls downloads/

# Verificar permisos
chmod 755 downloads
```

## 🎯 Características

- ✅ Interfaz interactiva por terminal
- ✅ Progreso en tiempo real con barra visual
- ✅ Múltiples estrategias de fallback (403/400)
- ✅ Descarga video (MP4) y audio (MP3)
- ✅ Archivos en `./downloads/` de tu máquina
- ✅ Docker Compose para instalación simple

## 📄 Licencia

MIT License

---

**Comando principal:** `./yt-downloader.sh`
