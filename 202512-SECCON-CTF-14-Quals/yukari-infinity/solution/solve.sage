from ptrlib import *
from Crypto.Util.number import *

a_list = list(range(2, 100, 2))
L = 1
for a in a_list:
    L = L*a//gcd(a,L)

for __ in range(10):
    sock = Process(["python3", "chal.py"])
    Q = 128
    for _ in range(Q):
        print(_)
        p = int(sock.recvlineafter("p = "))

        m = 1
        while True:
            if (p-1)%(2*m)!=0:
                break
            m *= 2
        print(m, p)
        K = CyclotomicField(min(m, 16))

        I = K.ideal(p)
        I = factor(I)[0][0]
        p0 = I.gens_reduced()[0]
        for k in range(10000):
            p0 += L
            q = int(p0.norm())
            if is_prime(q) and q%m==1 and q%(2*m)!=1:
                ok = True
                for a in a_list:
                    ap = pow(a, (p-1)//m, p)
                    aq = pow(a, (q-1)//m, q)
                    cp, cq = 0, 0
                    while ap!=1:
                        ap = ap*ap%p
                        cp += 1
                    while aq!=1:
                        aq = aq*aq%q
                        cq += 1
                    if cp != cq:
                        ok = False
                        break
                if ok:
                    print(q)
                    sock.sendlineafter("q: ", str(q))
                    print(sock.recvline())
                    break
        else:
            sock.close()
            break
    else:
        print(sock.recvline())
        exit()
