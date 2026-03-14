# As-Is Documentation — YouTube Downloader

> **Objetivo:** Documentar todas las piezas del sistema para que el tech lead comprenda el estado actual (As-Is).

---

## 1. Resumen Ejecutivo

| Aspecto | Descripción |
|---------|-------------|
| **Tipo** | Aplicación CLI interactiva para descargar videos/audio de YouTube |
| **Arquitectura** | Monolito Python, un solo módulo, contenedor Docker |
| **Despliegue** | Docker Compose, un contenedor |
| **Estado** | Sin estado; descargas en volumen montado |
| **Testing** | No hay tests automatizados |
| **CI/CD** | No configurado |
| **Logging** | Salida por `print`, sin logging estructurado |

---

## 2. Estructura del Proyecto

```
yt-downloader/
├── main.py              # Lógica de la aplicación
├── yt-downloader.sh     # Punto de entrada CLI (wrapper de Docker)
├── docker-compose.yml   # Configuración Docker Compose
├── Dockerfile           # Definición de la imagen
├── requirements.txt    # Dependencias Python
├── README.md            # Documentación de usuario
├── .gitignore           # Reglas de Git
├── docs/                # Documentación técnica
│   └── AS_IS.md         # Este documento
└── downloads/           # Salida de descargas (volumen montado)
    └── .gitkeep
```

---

## 3. Stack Tecnológico

| Tecnología | Versión/Uso |
|------------|-------------|
| **Python** | 3.12 (imagen base Docker) |
| **yt-dlp** | ≥2025.9.26 — motor de descarga de YouTube |
| **FFmpeg** | Paquete del sistema — conversión de audio a MP3 |
| **Docker** | Runtime de contenedores |
| **Docker Compose** | Orquestación de contenedores |

**Librerías estándar:** `os`, `sys`, `pathlib`, `time`, `random`, `datetime`, `urllib.parse`

---

## 4. Componentes Principales

### 4.1 `main.py` — Lógica de la Aplicación

| Función | Propósito |
|---------|-----------|
| `clean_youtube_url(url)` | Normaliza URLs de YouTube (quita playlist, parámetros extra; soporta youtu.be) |
| `progress_hook(d)` | Barra de progreso en tiempo real (%, MB, velocidad, ETA) |
| `create_robust_opts(output_dir, format_selector, show_progress)` | Construye opciones de yt-dlp (reintentos, headers, formato) |
| `download_with_fallback(url, output_dir, is_audio)` | Descarga con varias estrategias de formato en caso de fallo |
| `get_video_info_safe(url)` | Obtiene metadatos del video (título, duración) |
| `print_banner()` / `print_menu()` | Ayudas de UI en consola |
| `interactive_mode()` | Bucle principal interactivo (menú, URL, descargas) |
| `main()` | Punto de entrada: argumentos CLI o modo interactivo |

### 4.2 Comportamiento de Descarga

- **Video (MP4):** Mejor MP4 hasta 1080p → 720p → 480p → 360p
- **Audio (MP3):** Mejor audio → M4A → MP3 (192 kbps vía FFmpeg)
- **Fallback:** 3 estrategias por tipo, espera 5–10 s entre intentos
- **Solo un video:** `noplaylist: True` — no descarga playlists

### 4.3 `yt-downloader.sh`

- Comprueba que Docker esté instalado y en ejecución
- Comprueba que el contenedor `yt-downloader` esté corriendo
- Ejecuta `docker exec -it yt-downloader python main.py` para uso interactivo

---

## 5. Archivos de Configuración

### 5.1 `docker-compose.yml`

```yaml
services:
  yt-downloader:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: yt-downloader
    image: yt-downloader:latest
    volumes: ./downloads:/downloads:rw
    environment: PYTHONUNBUFFERED=1
    stdin_open: true
    tty: true
    entrypoint: ["python", "main.py"]
```

- Un solo servicio `yt-downloader`
- Volumen: `./downloads` → `/downloads` (lectura/escritura)
- Salida de Python sin buffer para logs en vivo
- TTY interactivo para entrada de usuario

### 5.2 `Dockerfile`

- Base: `python:3.12-slim`
- Instala FFmpeg y dependencias Python
- `WORKDIR`: `/app`
- Crea `/downloads` con `chmod 777`
- Ejecuta como root (sin usuario no-root)
- Entrypoint: `python main.py`

### 5.3 `.gitignore`

- Artefactos Python, venvs, archivos de IDE
- `downloads/*` (mantiene `downloads/.gitkeep`)
- Tests, cobertura, overrides de Docker, logs

---

## 6. Dependencias

### `requirements.txt`

```
yt-dlp>=2025.9.26
```

- Una sola dependencia directa: `yt-dlp`
- FFmpeg se instala en la imagen para conversión a MP3

---

## 7. Puntos de Entrada y Flujos

### 7.1 Flujo de Usuario

1. `docker-compose up -d` — construir y arrancar contenedor
2. `./yt-downloader.sh` — abrir aplicación interactiva dentro del contenedor

### 7.2 Cadena de Ejecución

```
./yt-downloader.sh
  → docker exec -it yt-downloader python main.py
    → main() en main.py
      → interactive_mode() (por defecto)
```

### 7.3 Modo CLI (alternativo)

```bash
docker exec -it yt-downloader python main.py <URL> [video|audio|both]
```

- `video` — solo MP4
- `audio` — solo MP3
- `both` — MP4 + MP3 (por defecto)

### 7.4 Directorio de Salida

- Dentro del contenedor: `/downloads`
- En el host: `./downloads` (vía volumen)

---

## 8. Detalles de Implementación

| Aspecto | Detalle |
|---------|---------|
| **URLs** | `clean_youtube_url()` elimina playlist y parámetros extra |
| **Reintentos** | 5 extractor, 10 descarga, 10 fragmentos |
| **Headers** | User-Agent y headers HTTP personalizados para reducir bloqueos |
| **Throttling** | Delay aleatorio 1–3 s antes de descargas; 5–10 s entre fallbacks |
| **Progreso** | Barra de una línea con `\r` y `flush=True` |
| **Escritura** | `interactive_mode()` comprueba permisos en `/downloads` antes de usar |

---

## 9. Diagrama de Flujo Simplificado

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  yt-downloader  │────▶│  Docker exec     │────▶│  main.py        │
│  .sh            │     │  yt-downloader   │     │  main()         │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                           │
                                    ┌──────────────────────┼──────────────────────┐
                                    │                      │                      │
                                    ▼                      ▼                      ▼
                           ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
                           │ CLI args       │    │ interactive_   │    │ yt-dlp         │
                           │ (video/audio/  │    │ mode()         │    │ download       │
                           │  both)         │    │                │    │                │
                           └────────────────┘    └────────────────┘    └────────────────┘
                                    │                      │                      │
                                    └──────────────────────┼──────────────────────┘
                                                           │
                                                           ▼
                                                  ┌────────────────┐
                                                  │ /downloads     │
                                                  │ (volumen)      │
                                                  └────────────────┘
```

---

## 10. Consideraciones de Seguridad y Operación

| Aspecto | Estado Actual |
|---------|---------------|
| **Usuario en contenedor** | root |
| **Autenticación** | No hay |
| **Rate limiting** | No implementado |
| **Permisos de volumen** | 777 en `/downloads` |
| **Variables de entorno** | Solo `PYTHONUNBUFFERED` |

---

## 11. Documentación Existente

- **README.md:** Instalación, uso, menú, ejemplo de progreso, comandos Docker, estructura, troubleshooting, características, licencia MIT

---

## 12. Resumen para el Tech Lead

- **Qué es:** Herramienta CLI para descargar videos/audio de YouTube en MP4/MP3.
- **Cómo se ejecuta:** Docker Compose + script `yt-downloader.sh` que hace `docker exec`.
- **Dónde está el código:** `main.py` (único módulo de aplicación).
- **Dependencias externas:** `yt-dlp`, FFmpeg.
- **Persistencia:** Solo el directorio `downloads` montado como volumen.
- **Testing/CI:** No hay tests ni pipeline de CI/CD.
- **Logging:** Solo `print`, sin niveles ni formato estructurado.

---

*Documento generado para AIM-30 — Documentación As-Is*
