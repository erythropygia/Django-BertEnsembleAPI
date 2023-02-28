FROM python:3.11.2 as base

RUN apt update && apt install -y --no-install-recommends gdal-bin \
    && apt install -y --no-install-recommends --fix-missing openssh-server \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt

WORKDIR /cer-nlp

RUN export PYTHONPATH="${PYTHONPATH}:/cer-nlp/"