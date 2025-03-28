FROM python:3.13

WORKDIR .

RUN apt-get update && \
    apt-get install -y gcc musl-dev libc-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]