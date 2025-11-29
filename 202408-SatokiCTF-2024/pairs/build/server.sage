import json
from Crypto.Util.number import getRandomNBitInteger

FLAG = b"flag{K0nka75u_D4m3dA><}"

r_upper = bin(getRandomNBitInteger(100))[2:]
print("upper 100 bits of r:", r_upper)

q = int(input("q: "))
r = int(input("r: "))
assert 256 <= q.bit_length() <= 600 and is_prime(q)
assert r.bit_length() == 256 and is_prime(r)
assert bin(r)[2:].startswith(r_upper)
assert 1 < q%r < r-1

F1 = GF(q)
a1 = F1(input("a1: "))
b1 = F1(input("b1: "))
assert a1 != F1(0) and b1 != F1(0)
E1 = EllipticCurve(F1, [a1, b1])

x1 = F1(input("x1: "))
y1 = F1(input("y1: "))
G1 = E1(x1, y1)
assert r*G1 == E1(0)

F2.<i> = GF(q^2, 'i', modulus=x^2+1)
a20, a21 = map(int, input("a2: ").split(','))
b20, b21 = map(int, input("b2: ").split(','))
a2 = F2(a20+a21*i)
b2 = F2(b20+b21*i)
assert a2 != F2(0) and b2 != F2(0)
E2 = EllipticCurve(F2, [a2, b2])

x20, x21 = map(int, input("x2: ").split(','))
y20, y21 = map(int, input("y2: ").split(','))
x2 = F2(x20+x21*i)
y2 = F2(y20+y21*i)
G2 = E2(x2, y2)
assert r*G2 == E2(0)

def to_dict(P):
    if P.base_ring() == F1:
        return {'x': int(P[0]), 'y': int(P[1])}
    else:
        Px, Py = P[0].polynomial(), P[1].polynomial()
        return {'x': [int(Px[0]), int(Px[1])], 'y': [int(Py[0]), int(Py[1])]}

# Solve SECCON Beginners CTF 2024 - bless !
challenges = []
for c in FLAG:
    s, t = randrange(r), randrange(r)
    challenges.append({
        'P': to_dict(s*G1),
        'Q': to_dict(t*G2),
        'R': to_dict(c*s*t*G2)
    })

print(json.dumps(challenges))
