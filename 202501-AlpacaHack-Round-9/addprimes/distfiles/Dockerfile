FROM sagemath/sagemath:10.5

ENV DEBIAN_FRONTEND=noninteractive

USER root
RUN apt update && apt install -yqq socat

USER sage
RUN sage -pip install pycryptodome
ADD server.sage server.sage

WORKDIR /home/sage
CMD ["socat", "TCP-L:9999,fork,reuseaddr", "EXEC:'sage server.sage'"]
