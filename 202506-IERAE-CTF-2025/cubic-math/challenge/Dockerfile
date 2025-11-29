FROM sagemath/sagemath:10.6@sha256:19995db6194f4a4bab18ce9a88556fd15b9ed5e916b4504fefe618a7796ddbdb

RUN sudo apt-get -y update --fix-missing
RUN sudo apt-get -y upgrade
RUN sudo apt-get -y install socat

USER sage
WORKDIR /app

COPY server.sage ./server.sage
COPY flag.txt ./flag.txt

CMD ["socat", "tcp-l:12347,reuseaddr,fork", "EXEC:'sage server.sage'"]