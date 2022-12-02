FROM python:3.10.6-buster

COPY moviespred moviespred
COPY setup.py setup.py
COPY requirements.txt requirements.txt
COPY .env .env

RUN apt-get update
# RUN apt-get install libsndfile1-dev -y

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD uvicorn moviespred.interface.main:app --host 0.0.0.0 --port $PORT
