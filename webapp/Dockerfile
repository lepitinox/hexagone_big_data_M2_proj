FROM python:3.9

WORKDIR /app
COPY webapp/main.py main.py
COPY webapp/requirements.txt requirements.txt
COPY .env .env
COPY kafka_config.json kafka_config.json

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
