# syntax=docker/dockerfile:1
FROM python:3.10.5-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
EXPOSE 8000/tcp
WORKDIR /code
COPY requirements.txt /code/
RUN \
	apt-get update && \
	apt-get install -y ffmpeg libsm6 libxext6 gcc musl-dev postgresql-server-dev-all && \
	python3 -m pip install -r requirements.txt
COPY . /code/
#CMD exec gunicorn djangoapp.wsgi:application --bind 0.0.0.0:8000 --workers 3