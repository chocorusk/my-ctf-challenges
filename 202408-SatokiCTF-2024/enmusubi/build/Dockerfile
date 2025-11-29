FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN apt-get -y install socat python3 python3-pip
RUN pip3 install pycryptodome

COPY server.py /app/server.py

RUN chmod 755 -R /app
RUN adduser -u 1000 enmusubi
USER enmusubi

WORKDIR /app
CMD ["socat", "tcp-listen:5555,fork,reuseaddr", "exec:\"python3 server.py\""]
