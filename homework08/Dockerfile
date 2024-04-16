FROM ubuntu:20.04
FROM python:3.9

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip
RUN mkdir /app

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY /src/api.py /app/api.py
COPY /src/worker.py /app/worker.py
COPY /src/jobs.py /app/jobs.py

COPY /testsrc/test_api.py /app/test_api.py
COPY /testsrc/test_worker.py /app/test_worker.py
COPY /testsrc/test_jobs.py /app/test_jobs.py

CMD ["python", "api.py"]
