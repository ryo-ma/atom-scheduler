FROM python:3.7-alpine

MAINTAINER Ryota Sakamoto<saka_ro@yahoo.co.jp>

COPY ./app /opt/atom-scheduler

WORKDIR /opt/atom-scheduler

RUN apk update && \
    apk add --no-cache --virtual .build python3-dev build-base linux-headers pcre-dev && \
    pip install pipenv && \
    pipenv install --system && \
    apk del --purge .build && \
    rm -r /root/.cache

COPY docker-conf/entrypoint.sh /opt
COPY docker-conf/env /opt/env

RUN chmod a+x /opt/entrypoint.sh

ENTRYPOINT /opt/entrypoint.sh

