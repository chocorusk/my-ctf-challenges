import os
from ptrlib import *
from Crypto.Util.number import *
from tqdm import tqdm

progress = tqdm()
while True:
    progress.update()
    sock = remote(os.environ.get("HOST", "localhost"), int(os.environ.get("PORT", 9999)))
    n = int(sock.recvlineafter("n: "))
    e = int(sock.recvlineafter("e: "))
    m1 = 2
    c1 = pow(m1, e, n)
    sock.sendlineafter("ciphertext: ", str(c1))
    m2 = int(sock.recvlineafter("plaintext: "))
    p = gcd(m1-m2, n)
    if p==1 or p==n:
        sock.close()
        continue
    q = n//p

    c = int(sock.recvlineafter("encrypted flag: "))
    pari.addprimes(p)
    ms = mod(c, n).nth_root(e, all=True)
    for m in ms:
        m = long_to_bytes(int(m))
        if b"Alpaca" in m:
            print(m)
            exit()
