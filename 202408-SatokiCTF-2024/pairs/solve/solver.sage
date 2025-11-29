from gmpy2 import isqrt
from Crypto.Util.number import *
from ptrlib import *
import json

D = 19

client = Socket("nc localhost 4444")

client.recvuntil(b'upper 100 bits of r: ')
r_upper = int(client.recvline(), 2)
l = int(isqrt(int(r_upper*2**(256-100))))+1

while True:
    r = l**2+1
    if not isPrime(int(r)):
        l += 1
        continue
    t = l+1
    A = 4*r
    if A%D==0:
        l += 1
        continue
    B = (l-1)**2
    m0 = pow(int(A),int(-1),int(D))*B%D
    z0 = (A*m0-B)//D
    if kronecker(z0, r) != 1:
        l += 1
        continue
    R.<x> = PolynomialRing(GF(r))
    V = int((x^2-z0).roots()[0][0])
    if (V**2-z0)%4!=0:
        l += 1
        continue
    i0 = (V**2-z0)//A
    m = m0+i0*D
    n = m*r
    q = n+t-1
    if q%4==3 and isPrime(q):
        break
    l += 1

print(q)
print(r)

client.sendline(str(q).encode())
client.sendline(str(r).encode())

H = QuadraticField(-D).hilbert_class_polynomial()
F1 = GF(q)
R1.<x> = PolynomialRing(F1)
H = R1(H)
j = H.roots()[0][0]
k = j*(1728-j)^(-1)
a1 = 3*k
b1 = 2*k
E1 = EllipticCurve(F1, [a1, b1])
n1 = E1.order()
if n1 > q+1:
    s1 = 2
    while True:
        if kronecker(s1, q) == -1:
            break
        s1 += 1
    a1 = a1*s1^2
    b1 = b1*s1^3
    E1 = EllipticCurve(F1, [a1, b1])
    n1 = E1.order()
assert n1%r == 0

G1 = E1.random_point()
G1 = n1//r*G1

print(a1)
print(b1)
print(G1)

client.sendline(str(a1).encode())
client.sendline(str(b1).encode())
client.sendline(str(G1[0]).encode())
client.sendline(str(G1[1]).encode())

F2.<i> = GF(q^2, "i", x^2 + 1)
R2.<y>=PolynomialRing(F2)
d0 = 1
while True:
    d = F2(d0)+i
    if len(R2(y^2-d).roots())==0:
        break
    d0 += 1

a2 = a1*d^2
b2 = b1*d^3
E2 = EllipticCurve(F2, [a2, b2])
G2 = E2.random_point()
n2 = E2.order()
assert n2%r==0
G2 = n2//r*G2

print(a2)
print(b2)
print(G2)

client.sendline((str(a2.polynomial()[0])+','+str(a2.polynomial()[1])).encode())
client.sendline((str(b2.polynomial()[0])+','+str(b2.polynomial()[1])).encode())
client.sendline((str(G2[0].polynomial()[0])+','+str(G2[0].polynomial()[1])).encode())
client.sendline((str(G2[1].polynomial()[0])+','+str(G2[1].polynomial()[1])).encode())

res = client.recvline()
res = res[res.index(b'['):]
output = json.loads(res)

F4.<j> = GF(q^4, "j", (x^2-d0)^2+1)

def F2_to_F4(v):
    v0 = v.polynomial()[0]
    v1 = v.polynomial()[1]
    return v0 + v1*(j^2-d0)

def pairing(P1, P2):
    E = EllipticCurve(F4, [a1, b1])
    P12 = E(P1[0], P1[1])
    P22 = E(F2_to_F4(P2[0])*j^(-2), F2_to_F4(P2[1])*j^(-3))
    return P12.weil_pairing(P22, r)

flag = ""
for _ in range(len(output)):
    Px = int(output[_]["P"]["x"])
    Py = int(output[_]["P"]["y"])
    Qx = (int(output[_]["Q"]["x"][0]),int(output[_]["Q"]["x"][1]))
    Qy = (int(output[_]["Q"]["y"][0]),int(output[_]["Q"]["y"][1]))
    Rx = (int(output[_]["R"]["x"][0]),int(output[_]["R"]["x"][1]))
    Ry = (int(output[_]["R"]["y"][0]),int(output[_]["R"]["y"][1]))

    P = E1(Px, Py)
    Q = E2(Qx[0]+Qx[1]*i, Qy[0]+Qy[1]*i)
    R = E2(Rx[0]+Rx[1]*i, Ry[0]+Ry[1]*i)
    pair1 = pairing(P, Q)
    pair2 = pairing(G1, R)
     
    for c in range(0x20, 0x80):
        if pair1^c == pair2:
            flag += chr(c)
            break
    print(flag)
