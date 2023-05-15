FROM python:3.10.8
WORKDIR /code
COPY requirements.txt requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN apt-get update && apt-get install memcached
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENTRYPOINT ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]