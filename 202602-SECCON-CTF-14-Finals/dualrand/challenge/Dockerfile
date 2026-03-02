FROM python:3.14.3-alpine@sha256:faee120f7885a06fcc9677922331391fa690d911c020abb9e8025ff3d908e510 as app

FROM pwn.red/jail
COPY --from=app / /srv

RUN mkdir /srv/app

COPY chal.py /srv/app/run
COPY ./flag.txt /srv/app/

RUN chmod 555 /srv/app/run
RUN chmod 444 /srv/app/flag.txt

ENV JAIL_CPU=100 JAIL_MEM=20M JAIL_TIME=30 JAIL_PORT=10395
EXPOSE 10395