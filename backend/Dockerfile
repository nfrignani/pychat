FROM python:3.9-slim

WORKDIR /app

RUN apt-get update
RUN apt-get install -y mariadb-client
RUN rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x wait-for-db.sh

CMD ["python", "app.py"]