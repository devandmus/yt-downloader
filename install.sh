#!/bin/bash

# YouTube Downloader - Script de Instalación
# Este script instala todas las dependencias necesarias

echo "🎥 YouTube Downloader - Instalador"
echo "=================================="
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instala Python 3.7 o superior."
    exit 1
fi

echo "✅ Python 3 encontrado: $(python3 --version)"

# Verificar si pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no está instalado. Por favor instala pip."
    exit 1
fi

echo "✅ pip3 encontrado: $(pip3 --version)"

# Instalar dependencias
echo ""
echo "📦 Instalando dependencias..."
echo ""

pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ ¡Instalación completada exitosamente!"
    echo ""
    echo "🚀 Para ejecutar la aplicación, usa:"
    echo "   python3 youtube_downloader.py"
    echo ""
    echo "📁 Los archivos se descargarán en: ~/Downloads"
    echo ""
else
    echo ""
    echo "❌ Error durante la instalación. Por favor revisa los errores arriba."
    exit 1
fi
