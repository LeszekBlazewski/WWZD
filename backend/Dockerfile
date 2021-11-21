FROM python:3.9-slim-buster as dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

VOLUME [ "/app" ]

CMD ["python", "app.py"]

FROM python:3.9-slim-buster as prod
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
