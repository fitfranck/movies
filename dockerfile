FROM tensorflow/tensorflow:2.10.0

COPY api api
COPY requirements.prod.txt requirements.txt

RUN apt-get update

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD uvicorn api.main:app --host 0.0.0.0 --port $PORT
