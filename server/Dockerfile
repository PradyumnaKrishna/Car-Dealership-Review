FROM python:3.8-slim

LABEL maintainer=PradyumnaKrishna

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /app
COPY . /app

CMD gunicorn --bind 0.0.0.0:$PORT myproject.wsgi