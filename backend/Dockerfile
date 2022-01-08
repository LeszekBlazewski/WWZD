FROM python:3.7-slim-buster as base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

ARG MODEL_ADDRESS=https://drive.google.com/uc?id=19CtF7rICsT0bbpisbn1t5CIxHG1USxh4
ARG DATASETS_ADDRESS=https://drive.google.com/uc?id=1-SFFXLXYvE13JsigqnP-QVFTDOczvb30
ENV ASSETS_PATH=/assets
ENV DATASETS_PATH=${ASSETS_PATH}/datasets
ENV PYTHONUNBUFFERED=1

RUN mkdir -p ${ASSETS_PATH} ${DATASETS_PATH} && \
    cd ${ASSETS_PATH} && \
    # download bert model
    gdown ${MODEL_ADDRESS} -O - --quiet | tar zxvf - && \
    cd ${DATASETS_PATH} && \
    # download datasets (json files + PCA/UMAP learned models)
    gdown ${DATASETS_ADDRESS} -O - --quiet | tar zxvf -

FROM base as prod

COPY . .
