#!/bin/bash

# YouTube Downloader - Instalador Completo
# Instala todas las dependencias del sistema y Python

echo "🎥 YouTube Downloader - Instalador Completo"
echo "=========================================="
echo ""

# Función para detectar el sistema operativo
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)
echo "🖥️  Sistema detectado: $OS"

# Verificar Python
echo ""
echo "🐍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instala Python 3.7 o superior."
    echo "   Descarga desde: https://python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python encontrado: $(python3 --version)"

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no está instalado. Instalando..."
    python3 -m ensurepip --upgrade
fi
echo "✅ pip encontrado: $(pip3 --version)"

# Verificar FFmpeg
echo ""
echo "🎬 Verificando FFmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg no está instalado. Instalando..."
    
    case $OS in
        "macos")
            if command -v brew &> /dev/null; then
                echo "📦 Instalando FFmpeg con Homebrew..."
                brew install ffmpeg
            else
                echo "❌ Homebrew no está instalado."
                echo "   Instala Homebrew: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
                echo "   Luego ejecuta: brew install ffmpeg"
                exit 1
            fi
            ;;
        "linux")
            echo "📦 Instalando FFmpeg con apt..."
            sudo apt update && sudo apt install -y ffmpeg
            ;;
        "windows")
            echo "❌ En Windows, instala FFmpeg manualmente:"
            echo "   1. Descarga desde: https://ffmpeg.org/download.html"
            echo "   2. Agrega FFmpeg al PATH del sistema"
            exit 1
            ;;
        *)
            echo "❌ Sistema operativo no soportado para instalación automática."
            echo "   Instala FFmpeg manualmente desde: https://ffmpeg.org/download.html"
            exit 1
            ;;
    esac
else
    echo "✅ FFmpeg encontrado: $(ffmpeg -version | head -n1)"
fi

# Crear entorno virtual
echo ""
echo "🏠 Creando entorno virtual..."
if [ -d "venv" ]; then
    echo "⚠️  El entorno virtual ya existe. Eliminando..."
    rm -rf venv
fi

python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "❌ Error creando entorno virtual"
    exit 1
fi
echo "✅ Entorno virtual creado"

# Activar entorno virtual e instalar dependencias
echo ""
echo "📦 Instalando dependencias de Python..."
source venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 ¡Instalación completada exitosamente!"
    echo ""
    echo "🚀 Para usar el downloader:"
    echo "   source venv/bin/activate"
    echo "   python main.py 'URL' audio"
    echo ""
    echo "📖 Para más información, lee README.md"
    echo ""
    echo "✨ ¡Disfruta descargando videos de YouTube!"
else
    echo ""
    echo "❌ Error durante la instalación de dependencias."
    echo "   Revisa los errores arriba y vuelve a intentar."
    exit 1
fi