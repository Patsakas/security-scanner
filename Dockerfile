FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir pygame==2.5.2
COPY app.py .
CMD ["python", "app.py"]
