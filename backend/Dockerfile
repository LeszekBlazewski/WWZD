FROM python:3.9-alpine as dev

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 5000

VOLUME [ "/app" ]

CMD ["python", "app.py"]

FROM python:3.9-alpine as prod
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
