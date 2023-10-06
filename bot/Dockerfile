FROM python:3.8-slim-buster

WORKDIR /

COPY . .

COPY ../.env /app

RUN pip3 install -r requirements.txt

CMD ["app/app.py"]
ENTRYPOINT ["python3"]
