FROM python:3.7

RUN apt-get update && apt-get -qy install netcat

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ./entrypoint.sh
