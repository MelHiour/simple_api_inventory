# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src/helpers.py helpers.py
COPY src/simple_inventory.py simple_inventory.py

RUN mkdir data

CMD [ "python3", "simple_inventory.py"]
