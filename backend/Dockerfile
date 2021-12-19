FROM python:3.9-slim-buster as base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

ARG MODELS_ADDRESS=https://drive.google.com/uc?id=1KxdXfduzTdl2n7JDB-ZomYxP6Zx5yVLE
ARG DATASETS_ADDRESS=https://drive.google.com/uc?id=1Y1E-WjcEHygYUdcrqGUKlIdZcrVcrPD0
ENV MODELS_PATH=/assets/models
ENV DATASETS_PATH=/assets/datasets
ENV PYTHONUNBUFFERED=1

RUN mkdir -p ${MODELS_PATH} ${DATASETS_PATH} && \
    cd ${MODELS_PATH} && \
    # download model (BERT + pickled umap and PCA) and extract them
    gdown ${MODELS_ADDRESS} -O - --quiet | tar zxvf - && \
    cd ${DATASETS_PATH} && \
    # download datasets (json files)
    gdown ${DATASETS_ADDRESS} -O - --quiet | tar zxvf -

FROM base as prod

COPY . .
