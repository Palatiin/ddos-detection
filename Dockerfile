FROM python:3.11-slim-bookworm

RUN apt-get update && \
    apt-get install -y iproute2 net-tools && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY attacks/slowloris.py .

CMD ["python3", "slowloris.py"]

