FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el contenido de la carpeta "app" correctamente
COPY . .

CMD ["python", "app.py"]
