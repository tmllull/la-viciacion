FROM python:3.11-slim-bookworm

ENV TZ=Europe/London

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "5000"]
