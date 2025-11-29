# https://eprint.iacr.org/2011/590.pdf

N = 509
q = 2048
p = 3
d = 253

Zx.<x> = ZZ[]

def invertmodprime(f,p):
    T = Zx.change_ring(Integers(p)).quotient(x^N-1)
    return Zx(lift(1 / T(f)))

def invertmodpowerof2(f,q):
    assert q.is_power_of(2)
    h = invertmodprime(f,2)
    while True:
        r = balancedmod(convolution(h,f),q)
        if r == 1: return h
        h = balancedmod(convolution(h,2 - r),q)

def balancedmod(f,q):
    g = list(((f[i] + q//2) % q) - q//2 for i in range(N))
    return Zx(g)

def convolution(f,g):
    return (f * g) % (x^N-1)

one = sum(x^i for i in range(N))

with open('../distfiles/output.txt') as f:
    public_keys = sage_eval(f.readline()[len("public keys: "):].strip(), locals={'x':x})
    ciphertexts = sage_eval(f.readline()[len("ciphertexts: "):].strip(), locals={'x':x})
    enc_flag = bytes.fromhex(f.readline()[len("encrypted flag: "):].strip())

mat = []
vec = []
for h, c in zip(public_keys, ciphertexts):
    try:
        h1 = invertmodpowerof2(h, q)
    except:
        continue
    h1 *= 2
    b = balancedmod(convolution(h1,c)-one, q)

    ht = list(h1)
    ht += [0]*(N-len(ht))
    ht = ht[::-1]
    ht = Zx([ht[-1]]+ht[:-1])
    a = balancedmod(convolution(ht,h1), q)
    w = balancedmod(convolution(ht,b), q)

    d0 = N
    s = (d0-sum(v*v for v in list(b)))%q

    a = list(a)
    w = list(w)
    a += [0]*(N-len(a))
    w += [0]*(N-len(w))

    vec.append(s)
    mat.append([a[0]]+[2*a[i] for i in range(1,N//2+1)]+[-2*w[i] for i in range(N)])

mat = matrix(Zmod(q), mat)
vec = vector(Zmod(q), vec)

print('solving...')
res = mat.solve_right(vec)
print(res)
res = [int(v) for v in list(res)[-N:]]
msg = balancedmod(res, 4)

from Crypto.Cipher import AES
from hashlib import sha256

key = sha256(str(msg).encode()).digest()[:16]
cipher = AES.new(key=key, mode=AES.MODE_CTR, nonce=enc_flag[:8])
flag = cipher.decrypt(enc_flag[8:])
print(flag)
