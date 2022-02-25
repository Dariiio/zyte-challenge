FROM python:3.10.2-slim-buster


WORKDIR /usr/src/scraper


COPY requirements.txt .


RUN pip install  --no-cache-dir -r requirements.txt
