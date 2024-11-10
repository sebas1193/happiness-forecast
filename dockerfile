FROM python:3.12

WORKDIR /app

# Copiar solo requirements.txt para instalar dependencias
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

CMD [ "python" "kafka_consumer.py" ]