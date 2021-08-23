FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /code
COPY *.py /code/
WORKDIR /code
ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "entrypoints.fastapi_app:app", "--host", "0.0.0.0", "--port", "80"]
