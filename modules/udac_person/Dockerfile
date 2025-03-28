FROM python:3.13-slim

WORKDIR /app

# Install compiler and PostgreSQL dev tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev && \  
    apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000 5001

CMD ["python", "wsgi.py"]
