#!/bin/sh

unzip Reference_Implementation.2024.10.10.1.zip
patch -p1 -d Reference_Implementation < diff-solve.patch
cd Reference_Implementation
g++ -shared -fPIC -m64 -O3 *.c ntl.cpp FromNIST/rng.c -I. -I/include -L/lib -std=c++11 -lcrypto -lssl -lm -ldl -lntl -lgmp -lgf2x -lpthread -DNIST_RAND=1 -o libbike-solve.so
cp libbike-solve.so ..
cd ..
