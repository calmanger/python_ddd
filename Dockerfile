FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10

# building greenlet needs g++ and make
RUN apk add --no-cache --virtual .build-deps gcc g++ postgresql-dev musl-dev python3-dev
RUN apk add libpq

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN apk del --no-cache .build-deps

RUN mkdir -p /src
COPY src/ /src/
RUN pip install -e /src
COPY tests/ /tests/

WORKDIR /src
