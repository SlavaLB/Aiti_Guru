FROM python:3.12

WORKDIR .

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --default-timeout=100 --no-cache-dir -r requirements.txt

COPY . .
