FROM python:3.11

WORKDIR /app
ENV PYTHONPATH /app

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/src/test

CMD ["pytest", ".", "-sv"]