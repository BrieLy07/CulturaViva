FROM python:3.12-slim

WORKDIR /app

# Dependencias del sistema necesarias
# RUN apt-get update && apt-get install -y \
#     git \
#     libglib2.0-0 \
#     libsm6 \
#     libxrender1 \
#     libxext6 \
#     build-essential \
#     python3-dev \
#     && rm -rf /var/lib/apt/lists/*

# Instalar torch primero (CPU compatible)
# RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Instalar el resto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el contenido de la carpeta "app" correctamente
COPY . .

CMD ["python", "app.py"]
