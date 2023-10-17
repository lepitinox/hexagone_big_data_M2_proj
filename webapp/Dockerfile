FROM python:3.9

WORKDIR /app
COPY webapp/main.py main.py
COPY webapp/requirements.txt requirements.txt
COPY .env .env

RUN pip install -r requirements.txt

CMD ["streamlit", "run","main.py","--server.port=80", "--server.address=0.0.0.0"]
