FROM python:3.9

WORKDIR /app

COPY . .

# COPY .env /app

RUN pip3 install -r requirements.txt

CMD ["app/app.py"]
ENTRYPOINT ["python3"]
