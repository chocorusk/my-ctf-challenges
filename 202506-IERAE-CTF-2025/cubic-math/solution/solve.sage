from ptrlib import *

sock = Process(["sage", "../challenge/server.sage"])

def del2(f):
    R.<x> = PolynomialRing(ZZ)
    coeffs = f.list()
    c1 = 9*coeffs[1]-3*coeffs[2]^2
    c0 = 27*coeffs[0]-coeffs[2]^3-coeffs[2]*(9*coeffs[1]-3*coeffs[2]^2)
    return c1, c0

cnt = 0

res_all = set()
while len(res_all)<10:
    a, b = randrange(2**31), randrange(2**31)
    sock.sendlineafter("a, b = ", str(a)+","+str(b))
    res = eval(sock.recvline())
    res_all |= set(res)
    cnt += 1
print(res_all)

qs = []
rs = []
qs2 = []
rs2 = []
for q in range(7, 600, 3):
    if not is_prime(q):
        continue
    if cnt>=49:
        break

    K = CyclotomicField(q)
    k = K.subfields(3)[0][0]
    assert k.conductor()==q
    print(q)
    f = k.polynomial()
    a, b = del2(f)
    print(a, b)
    sock.sendlineafter("a, b = ", str(a)+","+str(b))
    res = eval(sock.recvline())
    cnt += 1
    
    irrs = []
    for i in range(1, q):
        qi = -1
        for j in range(i, 10**9, q):
            if is_prime(j):
                qi = j
                break
        R.<x> = PolynomialRing(GF(qi))
        if R(f).is_irreducible():
            irrs.append(i)

    kouho = []
    for i in range(q):
        dame = False
        for r in res_all:
            if (r+i)%q==0:
                dame=True
                break
            if r in res:
                if not ((r+i)%q in irrs):
                    dame=True
                    break
            else:
                if (r+i)%q in irrs:
                    dame=True
                    break
        if not dame:
            kouho.append(i)
    print(kouho)
    if len(kouho)==1:
        qs.append(q)
        rs.append(kouho[0])
    elif len(kouho)==2:
        qs2.append(q)
        rs2.append(kouho)

if len(qs2)>10:
    qs2 = qs2[-10:]
    rs2 = rs2[-10:]

print(int(prod(qs+qs2)).bit_length())
print(cnt)

for i in range(2**len(qs2)):
    rs2_ = []
    for j in range(len(qs2)):
        rs2_.append(rs2[j][(i>>j)&1])
    secret = CRT_list(rs+rs2_, qs+qs2)

    diffs = set()
    p = secret
    while len(diffs) < 10:
        p = next_prime(p)
        diffs.add(p-secret)
    
    if res_all == diffs:
        print(secret)
        break

sock.sendlineafter("a, b = ", str(secret)+",0")
sock.interactive()
