From ubuntu:16.04

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev
RUN apt-get install -y docker.io
RUN apt-get install -y libfribidi-bin

COPY ./database/requirements.txt /app/requirements.txt

COPY ./sample_config.json /app/sample_config.json

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python", "-u"]
CMD ["./database/database_accessor.py"]
