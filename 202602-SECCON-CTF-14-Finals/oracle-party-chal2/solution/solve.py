# about 220 queries

from ptrlib import *
from Crypto.Util.number import *
import random
import string
from itertools import product

min_query = 1000
for _ in range(100):
    sock = Socket("nc localhost 10002")
    sock.sendlineafter("team_id>", "team-token")

    n = int(sock.recvlineafter("n: "))
    ct_flag = int(sock.recvlineafter("encrypted secret: "))
    e = 65537

    ml = b"SECCON{" + b"A"*0x37 + b"}"
    ml = bytes_to_long(pad(ml, 16))
    mr = b"SECCON{" + b"z"*0x37 + b"}"
    mr = bytes_to_long(pad(mr, 16))

    cnt = 0
    while long_to_bytes(ml)[:59] != long_to_bytes(mr)[:59]:
        cnt += 1
        
        while True:
            l = random.randrange(int(ml/(mr-ml)*(2**(1024-8)/n)*3.0), int(ml/(mr-ml)*(2**(1024-8)/n)*3.1))
            kl = max(((l+1)*n+mr-1)//mr, (l*n+ml-1)//ml)
            kr = min(((l+1)*n+ml-1)//ml, ((l+2)*n+mr-1)//mr)
            k = random.randrange(kl, kr)
            
            if not (2**(1024-8)*1.9 < mr*k-(l+1)*n < 2**(1024-8)*2):
                continue
            
            m0 = (1*k-l*n)%256
            m1 = (m0-n)%256
            if (m0==0 or m0>16) and not (m1==0 or m1==1 or m1>16):
                ct = ct_flag*pow(k, e, n)%n
                sock.sendlineafter("ciphertext or guess: ", str(ct))
                res = sock.recvline()
                if b"Input data is not padded" in res:
                    ml = (n*(l+1)+k-1)//k
                    mr = (n*(l+1)+2**(1024-8)+k-1)//k
                elif b"Padding is incorrect." in res:
                    mr = (n*(l+1)+k-1)//k
                elif b"PKCS#7 padding is incorrect." in res:
                    ml = (n*(l+1)+2**(1024-8)+k-1)//k
                else:
                    continue
                break
            elif (m1==0 or m1>16) and not (m0==0 or m0==1 or m0>16):
                ct = ct_flag*pow(k, e, n)%n
                sock.sendlineafter("ciphertext or guess: ", str(ct))
                res = sock.recvline()
                if b"Input data is not padded" in res:
                    ml = (n*(l+1)+k-1)//k
                    mr = (n*(l+1)+2**(1024-8)+k-1)//k
                elif b"PKCS#7 padding is incorrect." in res:
                    mr = (n*(l+1)+k-1)//k
                elif b"Padding is incorrect." in res:
                    ml = (n*(l+1)+2**(1024-8)+k-1)//k
                else:
                    continue
                break
        
        ml_byte = long_to_bytes(ml)
        mr_byte = long_to_bytes(mr)
        for i in range(62):
            if ml_byte[i] != mr_byte[i]:
                if ml_byte[i] < ord("A"):
                    ml_byte = ml_byte[:i] + b"A"*(62-i) + b"}" + bytes([1]*1)
                if mr_byte[i] > ord("z"):
                    mr_byte = mr_byte[:i] + b"z"*(62-i) + b"}" + bytes([1]*1)
                break
        ml = bytes_to_long(ml_byte)
        mr = bytes_to_long(mr_byte)
    
    print(ml_byte)
    print(mr_byte)
    
    ans = None
    for c1 in string.ascii_letters:
        if ord(c1) < ml_byte[59] or mr_byte[59] < ord(c1):
            continue
        for c2 in product(string.ascii_letters, repeat=2):
            m = bytes_to_long(ml_byte[:59] + bytes([ord(c1)]+list(map(ord, c2))) + b"}\x01")
            if pow(m, e, n) == ct_flag:
                ans = long_to_bytes(m)[:62]+b"}"
                break
        if ans:
            break

    print(cnt, ans)
    sock.sendlineafter("ciphertext or guess: ", ans)
    
    if cnt < min_query:
        min_query = cnt
    print(min_query)
