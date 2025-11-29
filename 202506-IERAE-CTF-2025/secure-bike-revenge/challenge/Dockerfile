FROM python:3.13-slim@sha256:914bf5c12ea40a97a78b2bff97fbdb766cc36ec903bfb4358faf2b74d73b555b

RUN apt-get -y update --fix-missing
RUN apt-get -y upgrade
RUN apt-get -y install build-essential libssl-dev libntl-dev libgmp-dev libgf2x-dev unzip socat
RUN pip install --no-cache-dir pycryptodome

RUN useradd -d /home/ctf ctf
WORKDIR /home/ctf

# RUN wget https://bikesuite.org/files/v5.2/Reference_Implementation.2024.10.10.1.zip
COPY Reference_Implementation.2024.10.10.1.zip ./Reference_Implementation.2024.10.10.1.zip
RUN unzip Reference_Implementation.2024.10.10.1.zip

COPY diff.patch ./diff.patch
RUN patch -p1 -d Reference_Implementation < diff.patch

WORKDIR /home/ctf/Reference_Implementation
RUN g++ -shared -fPIC -m64 -O3 *.c ntl.cpp FromNIST/rng.c -I. -I/include -L/lib -std=c++11 -lcrypto -lssl -lm -ldl -lntl -lgmp -lgf2x -lpthread -DNIST_RAND=1 -o libbike.so
RUN cp libbike.so ..

WORKDIR /home/ctf
COPY server.py ./server.py
COPY flag.txt ./flag.txt

USER ctf
CMD ["socat", "tcp-l:12350,reuseaddr,fork", "EXEC:'python server.py'"]
