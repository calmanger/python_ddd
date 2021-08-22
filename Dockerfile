FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY *.py /code/
WORKDIR /code
ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "fastapi_app:app", "--host", "0.0.0.0", "--port", "80"]
