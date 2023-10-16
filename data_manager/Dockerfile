FROM python:3.9

WORKDIR /app
COPY data_manager/main.py main.py
COPY data_manager/requirements.txt requirements.txt
COPY .env .env
COPY kafka_config.json kafka_config.json

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
