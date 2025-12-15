FROM python:3.12-slim

# Metadata
LABEL maintainer="YouTube Downloader"
LABEL description="Descargador robusto de YouTube con streaming de progreso"

# Evitar preguntas interactivas durante la instalación
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar FFmpeg y dependencias del sistema en una sola capa
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY main.py .

# Crear directorio de descargas con permisos correctos
RUN mkdir -p /downloads && chmod 777 /downloads

# Usuario no-root para seguridad (opcional, pero recomendado)
USER root

# Punto de entrada
ENTRYPOINT ["python", "main.py"]



