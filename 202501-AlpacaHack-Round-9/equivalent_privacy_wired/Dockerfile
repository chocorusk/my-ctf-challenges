FROM python:3.13-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -yqq socat
RUN pip install pycryptodome
ADD rawdistfiles/server.py server.py

CMD ["socat", "TCP-L:9999,fork,reuseaddr", "EXEC:'python server.py'"]
