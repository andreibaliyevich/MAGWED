# syntax=docker/dockerfile:1
FROM postgres:16.2

RUN apt-get update \
    && apt-get install wget -y \
    && apt-get install postgresql-16-postgis-3 -y \
    && apt-get install postgis -y

COPY ./db.sql /docker-entrypoint-initdb.d/
