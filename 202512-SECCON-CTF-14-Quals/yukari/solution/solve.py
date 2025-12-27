from ptrlib import *
from Crypto.PublicKey import RSA
from Crypto.Util.number import *

sock = Process(["python3", "chal.py"])

for _ in range(32):
    p = int(sock.recvlineafter("p = "))

    q = 1
    while True:
        q += 2*p
        if isPrime(q):
            n = p * q
            e = getPrime(64)
            d = pow(e, -1, (p - 1) * (q - 1))

            try:
                cipher = RSA.construct((n, e, d))
            except:
                print(q)
                break
    
    sock.sendlineafter("q: ", str(q))
    print(sock.recvline())

print(sock.recvline())
