FROM python:3.9-slim-buster as base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

ARG MODEL_ADDRESS=https://drive.google.com/uc?id=1KxdXfduzTdl2n7JDB-ZomYxP6Zx5yVLE
ARG DATASETS_ADDRESS=https://drive.google.com/uc?id=1Y1E-WjcEHygYUdcrqGUKlIdZcrVcrPD0
ENV MODEL_PATH=/assets/model
ENV DATASETS_PATH=/assets/datasets
ENV PYTHONUNBUFFERED=1

RUN mkdir -p ${MODEL_PATH} ${DATASETS_PATH} && \
    cd ${MODEL_PATH} && \
    # download bert model
    gdown ${MODEL_ADDRESS} -O - --quiet | tar zxvf - && \
    cd ${DATASETS_PATH} && \
    # download datasets (json files + PCA/UMAP learned models)
    gdown ${DATASETS_ADDRESS} -O - --quiet | tar zxvf -

FROM base as prod

COPY . .
