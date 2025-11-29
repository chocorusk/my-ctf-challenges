from Crypto.Util.number import *

with open("../distfiles/output.txt") as f:
    sp0, sp1 = eval(f.readline().replace("your share of p: ", ""))
    sq0, sq1 = eval(f.readline().replace("your share of q: ", ""))
    spq0, spq1 = eval(f.readline().replace("your share of pq: ", ""))
    n = int(f.readline().replace("n: ", ""))
    e = int(f.readline().replace("e: ", ""))
    c = int(f.readline().replace("c: ", ""))

# p*q = n
# sp1*sq1+sp1*(q-sq0-sq1)+sq1*(p-sp0-sp1) = spq1+r
c2 = sq1
c1 = -sp1*sq0-sp0*sq1-sp1*sq1-spq1
c0 = sp1*n
if c2<0:
    c0, c1, c2 = -c0, -c1, -c2
def f(x):
    return c2*x**2+c1*x+c0

l = -2**600
r = -c1//(2*c2)
while r-l>1:
    mid = (l+r)//2
    if f(mid)>0:
        l = mid
    else:
        r = mid
r1, r2 = l, -c1//c2-l

for p in list(range(r1-1000, r1+1000)) + list(range(r2-1000, r2+1000)):
    if n%p==0:
        print(abs(r1-p), abs(r2-p))
        q = n//p
        d = pow(e, -1, (p-1)*(q-1))
        flag = long_to_bytes(pow(c, d, n))
        print(flag)
        break
