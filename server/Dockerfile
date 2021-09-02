FROM python:3.8-slim

LABEL maintainer=PradyumnaKrishna

ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1
ENV APP=/app

RUN apt-get update && apt-get install -y libpq-dev gcc

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Change the workdir.
WORKDIR $APP
COPY . $APP

CMD gunicorn --bind 0.0.0.0:$PORT confs.wsgi
