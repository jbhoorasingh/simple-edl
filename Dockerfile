FROM python:3.10-buster AS builder
LABEL maintainer="Jermaine Bhoorasingh <simple-edl@jermaine.co>"

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
#RUN echo "net.ipv4.ping_group_range = 0 2147483647" >> /etc/sysctl.conf

# copy project
COPY . .