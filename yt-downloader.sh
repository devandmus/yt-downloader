#!/bin/bash

# YouTube Downloader - Abre el shell interactivo
# Asegúrate de haber levantado el contenedor con: docker-compose up -d

set -e

echo "🎥 YouTube Downloader"
echo "===================="
echo ""

# Verificar que Docker esté instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    echo "   Instala Docker desde: https://docs.docker.com/get-docker/"
    exit 1
fi

# Verificar que Docker esté corriendo
if ! docker info &> /dev/null; then
    echo "❌ Docker no está corriendo"
    echo "   Por favor inicia Docker Desktop o el servicio de Docker"
    exit 1
fi

# Verificar que el contenedor esté corriendo
if ! docker ps --format '{{.Names}}' | grep -q '^yt-downloader$'; then
    echo "❌ El contenedor 'yt-downloader' no está corriendo"
    echo ""
    echo "💡 Primero instala y levanta el contenedor con:"
    echo "   docker-compose up -d"
    echo ""
    exit 1
fi

echo "✅ Contenedor detectado"
echo ""
echo "===================================="
echo "🎉 Abriendo shell interactivo..."
echo "===================================="
echo "💡 Ingresa las URLs cuando se te pida"
echo "💡 Los archivos se guardarán en: ./downloads"
echo "💡 Para salir, presiona Ctrl+C o selecciona opción 4"
echo ""

# Conectar al contenedor de forma interactiva
exec docker exec -it yt-downloader python main.py
