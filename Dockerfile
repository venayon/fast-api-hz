FROM python:3.9-slim

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY ./app /src/app

ENV hazelcast_address="hazelcast_service:5701"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8081" ,"--log-level","info"]