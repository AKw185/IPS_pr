FROM python:3.11-alpine3.16
RUN pip install --no-cache-dir --upgrade pip==22.3.1
COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY Consumer/writer.py ./Consumer/
COPY . .

ENTRYPOINT ["python", "/app/Consumer/writer.py"]
