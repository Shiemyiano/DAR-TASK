FROM python:3.9-slim
WORKDIR /app
COPY ClientWrite.py .
RUN pip install opcua
CMD ["python", "ClientWrite.py"]