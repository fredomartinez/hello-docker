# Usamos la imagen oficial de Python como imágen padre
FROM python:2.7-slim

# Seteamos /app como directorio de trabajo
WORKDIR /app

# Copiamos el código de nuestra aplicación y sus dependencias en /app
COPY . .

# Instalamos los paquetes expecificados en requirements.txt
RUN pip install -r requirements.txt

# Exponemos el puerto 80
EXPOSE 80

# Definimos una variable de entorno
ENV NAME Bitlogic

# Cuando corramos esta imagen, por defecto se ejecutará este comando
CMD ["python", "app.py"]