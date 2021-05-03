FROM python:3.9-slim

ENV PIP_NO_CACHE_DIR=off \
PYTHONPATH=/usr/local/src/app

RUN apt-get update && apt-get install -y --no-install-recommends gcc

WORKDIR /usr/local/src/app

RUN pip install pipenv 

COPY api/Pipfile api/Pipfile.lock ./

RUN pipenv install --system

COPY ./ ./