FROM python:3.9-slim-buster as base

WORKDIR /app

ARG MODEL_ADDRESS=https://drive.google.com/uc?id=1DtTKNK4JP_LtWBDXAcN80VRhk-6oA11g
ENV MODEL_PATH=/model

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN mkdir -p ${MODEL_PATH} && \
    cd ${MODEL_PATH} && \
    # download our model and extract it inside the given directory directory
    gdown ${MODEL_ADDRESS} -O - --quiet | tar zxvf -

FROM base as prod

COPY . .
