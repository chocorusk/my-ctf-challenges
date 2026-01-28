import os
from random import SystemRandom

FLAG = os.getenv("FLAG", "Alpaca{dummy_flag!!!!!!!!!!!}").encode()
assert FLAG.startswith(b"Alpaca{") and FLAG.endswith(b"}")
flag = FLAG[7:-1]
assert len(flag) == 21

n = 7
m = 10
p = 8380417
F = GF(p)

random = SystemRandom()

A = matrix(F, [[random.randrange(0, p) for _ in range(n)] for _ in range(m)])
s = vector(F, [int.from_bytes(flag[3*i:3*(i+1)], "big") for i in range(n)])
e = vector(F, [random.randrange(0, 2) for _ in range(m)])
b = A * s + e

print("A =", [v.list() for v in A])
print("b =", b.list())
