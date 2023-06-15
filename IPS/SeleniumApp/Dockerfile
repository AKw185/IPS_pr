FROM python:3.11-alpine3.16
RUN pip install --no-cache-dir --upgrade pip==22.3.1
COPY requirements.txt ./requirements.txt

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/SeleniumApp
COPY . .

EXPOSE 3000

ENTRYPOINT ["python", "main.py"]