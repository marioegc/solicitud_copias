# Usar una imagen base oficial de Python
FROM python:3.8-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos requeridos al contenedor
COPY requirements.txt .

# Instalar las dependencias
RUN pip install -r requirements.txt

# Copiar el resto de tu aplicación Flask al directorio de trabajo
COPY . .

# Exponer el puerto 7000 en el que se ejecutará la aplicación
EXPOSE 7000

# Comando para ejecutar la aplicación en el puerto 7000
CMD ["flask", "run", "--host=0.0.0.0", "--port=7000"]
