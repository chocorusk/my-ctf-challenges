import os
from Crypto.Util.number import getRandomRange, getPrime, bytes_to_long

FLAG = os.environ.get("FLAG", "fakeflag").encode()

def additive_share(a):
    t0, t1 = getRandomRange(-2**512, 2**512), getRandomRange(-2**512, 2**512)
    t2 = a-t0-t1
    return t0, t1, t2

def replicated_share(a):
    t = additive_share(a)
    return [(t[i], t[(i+1)%3]) for i in range(3)]

def multiply_shares(sa, sb):
    def mul(t, u):
        return t[0]*u[0]+t[0]*u[1]+t[1]*u[0]
    r = additive_share(0)
    z = [mul(sa[i], sb[i])+r[i] for i in range(3)]
    w = [(z[i], z[(i+1)%3]) for i in range(3)]
    return w

def reconstruct(s):
    return s[0][0] + s[0][1] + s[1][1]

p = getPrime(512)
q = getPrime(512)

sp = replicated_share(p)
sq = replicated_share(q)
print("your share of p:", sp[0])
print("your share of q:", sq[0])

spq = multiply_shares(sp, sq)
print("your share of pq:", spq[0])

n = reconstruct(spq)
assert n == p*q
print("n:", n)

e = 0x10001
c = pow(bytes_to_long(FLAG + os.urandom(127-len(FLAG))), e, n)
print("e:", e)
print("c:", c)
