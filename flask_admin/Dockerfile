# Usamos una imagen ligera de Python 3.12
FROM python:3.12-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos primero los requerimientos para aprovechar el caché de Docker
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código fuente del panel
COPY . .

# Variables de entorno por defecto para Flask
ENV FLASK_APP=run.py
ENV FLASK_DEBUG=1

# Exponemos el puerto estándar de Flask
EXPOSE 5000

# Comando para levantar el servidor permitiendo conexiones externas
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]