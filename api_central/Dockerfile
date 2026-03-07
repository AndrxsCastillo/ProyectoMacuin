# Usamos una imagen oficial de Python ligera
FROM python:3.12-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de requerimientos y los instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código de nuestra app
COPY ./app ./app

# Exponemos el puerto donde correrá FastAPI
EXPOSE 8000

# Comando para arrancar el servidor cuando el contenedor inicie
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]