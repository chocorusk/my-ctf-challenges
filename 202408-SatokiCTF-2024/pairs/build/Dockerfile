FROM sagemath/sagemath:10.4

USER root
RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN apt-get install -y socat
RUN sage -pip install pycryptodome

COPY server.sage /app/server.sage

WORKDIR /app
CMD ["socat", "tcp-listen:4444,fork,reuseaddr", "exec:\"sage server.sage\""]
