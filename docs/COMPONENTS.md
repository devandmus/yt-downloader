# Referencia de Componentes — YouTube Downloader

Referencia rápida de cada pieza del sistema para el tech lead.

---

## Archivos de Código

### `main.py`

| Función | Líneas aprox. | Descripción |
|---------|----------------|-------------|
| `clean_youtube_url()` | 17-55 | Normaliza URLs de YouTube (youtu.be, playlist, query params) |
| `progress_hook()` | 56-86 | Callback de yt-dlp para barra de progreso en tiempo real |
| `create_robust_opts()` | 88-125 | Opciones de yt-dlp: retries, headers, format, noplaylist |
| `download_with_fallback()` | 126-182 | Descarga con 3 estrategias de formato en caso de fallo |
| `get_video_info_safe()` | 184-202 | Extrae metadata de video sin descargar |
| `print_banner()` | 204-211 | Banner de bienvenida |
| `print_menu()` | 213-222 | Menú de opciones 1-4 |
| `interactive_mode()` | 224-341 | Bucle principal: menú, URL, descargas, continuar |
| `main()` | 343-372 | Entry point: CLI args o interactive_mode() |

### `yt-downloader.sh`

| Sección | Comportamiento |
|---------|----------------|
| Líneas 13-24 | Verifica que Docker esté instalado |
| Líneas 21-24 | Verifica que Docker esté corriendo |
| Líneas 27-34 | Verifica que el contenedor `yt-downloader` exista |
| Línea 47 | `docker exec -it yt-downloader python main.py` |

---

## Archivos de Configuración

### `docker-compose.yml`

| Clave | Valor | Propósito |
|-------|-------|-----------|
| `build.context` | `.` | Contexto de build |
| `build.dockerfile` | `Dockerfile` | Archivo Docker |
| `container_name` | `yt-downloader` | Nombre fijo del contenedor |
| `image` | `yt-downloader:latest` | Tag de imagen |
| `volumes` | `./downloads:/downloads:rw` | Montaje de descargas |
| `environment.PYTHONUNBUFFERED` | `1` | Logs en tiempo real |
| `stdin_open` | `true` | Entrada interactiva |
| `tty` | `true` | TTY para modo interactivo |
| `entrypoint` | `["python", "main.py"]` | Comando por defecto |

### `Dockerfile`

| Paso | Comando/Acción |
|------|----------------|
| Base | `python:3.12-slim` |
| ENV | `DEBIAN_FRONTEND`, `PYTHONUNBUFFERED`, `PIP_*` |
| RUN | `apt-get install ffmpeg` |
| WORKDIR | `/app` |
| COPY | `requirements.txt` → pip install |
| COPY | `main.py` |
| RUN | `mkdir -p /downloads && chmod 777 /downloads` |
| USER | `root` |
| ENTRYPOINT | `python main.py` |

### `requirements.txt`

```
yt-dlp>=2025.9.26
```

---

## Directorios

| Carpeta | Propósito |
|---------|-----------|
| `downloads/` | Salida de descargas (volumen Docker) |
| `docs/` | Documentación técnica (AS_IS, COMPONENTS) |

---

## Estrategias de Formato (fallback)

### Video (MP4)

1. `best[ext=mp4][height<=1080]/best[ext=mp4]/mp4`
2. `best[height<=720]/mp4`
3. `best[height<=480]`
4. `worst[height<=360]`

### Audio (MP3)

1. `bestaudio[ext=m4a]/bestaudio/best[height<=720]`
2. `bestaudio/best[height<=480]`
3. `worst[height<=360]`

Post-procesador: FFmpegExtractAudio → MP3 @ 192 kbps

---

## Variables de Entorno

| Variable | Uso |
|----------|-----|
| `PYTHONUNBUFFERED` | Salida inmediata de print (sin buffer) |

---

## Rutas Importantes

| Ruta | Contexto | Descripción |
|------|----------|-------------|
| `/app` | Contenedor | WORKDIR, contiene main.py |
| `/downloads` | Contenedor | Destino de descargas |
| `./downloads` | Host | Montaje del volumen |

---

*Referencia para AIM-30 — Documentación As-Is*
