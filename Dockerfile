FROM python:3.9-slim
WORKDIR /app
COPY clientRead.py .
RUN pip install opcua paho-mqtt 
CMD ["python", "clientRead.py"]