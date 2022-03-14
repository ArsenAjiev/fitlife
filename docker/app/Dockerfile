FROM python:3.8-buster

WORKDIR /usr/src/app

# copy source code
COPY ./app .


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# fix for backports.zoneinfo
RUN apt-get update
RUN apt-get -y install libpq-dev gcc


RUN pip install --upgrade pip wheel
RUN pip install -r requirements.txt


COPY ./docker/app/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./docker/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

ENTRYPOINT ["/entrypoint.sh"]

