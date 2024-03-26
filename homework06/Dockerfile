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

COPY gene_api.py /app/gene_api.py

ENTRYPOINT ["python3"]
CMD ["gene_api.py"]
