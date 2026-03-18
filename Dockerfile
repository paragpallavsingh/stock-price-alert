FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ .
# Create a user so we don't run as root (Security!)
RUN useradd -m devopsuser
USER devopsuser
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
