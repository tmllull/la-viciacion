FROM python:3.11-slim-bookworm

ENV TZ=Europe/Madrid

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

CMD ["app/app.py"]
ENTRYPOINT ["python3"]
