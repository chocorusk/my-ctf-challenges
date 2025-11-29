from ptrlib import *
from ctypes import cdll, c_buffer
from Crypto.Cipher import AES

libbike = cdll.LoadLibrary('./libbike-solve.so')

n = 12323
d = 71
t = 134

R_BYTES = (n+7)//8
M_BYTES = 256//8
SS_BYTES = 256//8
N0 = 2

pk_size = R_BYTES
sk_size = R_BYTES * N0 + M_BYTES + M_BYTES
ct_size = R_BYTES + M_BYTES
ss_size = SS_BYTES
e_size = R_BYTES*N0

PR.<x> = PolynomialRing(GF(2))

def bytes_to_poly(b):
    f = 0
    for i in range(len(b)):
        for j in range(8):
            if 8*i+j<n and (b[i]>>j)&1:
                f += x^(8*i+j)
    return f

def poly_to_bytes(f):
    coeffs = f.list()
    b = [0]*R_BYTES
    for i in range(len(coeffs)):
        if coeffs[i]==1:
            b[i//8] ^^= (1<<(i%8))
    return bytes(b)

def poly_to_bits(f):
    coeffs = f.list()
    b = [0]*n
    for i in range(len(coeffs)):
        if coeffs[i]==1:
            b[i]=1
    return bytes(b)

def inverse(f):
    T = PR.quotient(x^n-1)
    return PR(lift(T(1)/T(f)))

sock = Process(["python3", "server.py"])

h = bytes.fromhex(sock.recvlineafter("public key: ").strip().decode())

h_inv = inverse(bytes_to_poly(h))

c = bytes.fromhex(sock.recvlineafter("ciphertext: ").strip().decode())
c = list(c)

hint = eval(sock.recvlineafter("hint: ").strip().decode())

sock.sendlineafter("ciphertext: ", bytes(c).hex())
enc_flag = bytes.fromhex(sock.recvlineafter("encrypted flag: ").strip().decode())
nonce, enc_flag = enc_flag[:8], enc_flag[8:]

b = 16

tb = 181
threshold = -1
e_hint = ""
e0 = 0
cnts = []
results = [[] for _ in range(2)]
for k in range(len(hint)):
    i = hint[k]
    if k>=b:
        i = (i-int(e_hint[k-b:k], 2))%n
        
    cnt = 0
    for _ in range(256):
        flips = random.sample(range(n), tb-t) + [i]
        for j in flips:
            c[j//8] ^^= (1<<(j%8))
        
        sock.sendlineafter("ciphertext: ", bytes(c).hex())
        res = sock.recvline()
        if b"error" not in res:
            cnt += 1

        for j in flips:
            c[j//8] ^^= (1<<(j%8))
    
    print(k, i, cnt, e_hint)
    cnts.append(cnt)

    if k>=b:
        if abs(cnt-ave0) < abs(cnt-ave1):
            e_hint += "0"
            results[0].append(cnt)
            ave0 = sum(results[0])/len(results[0])
        else:
            e_hint += "1"
            e0 += x^i
            results[1].append(cnt)
            ave1 = sum(results[1])/len(results[1])

    if k==b-1:
        cnts_sort = sorted(cnts)
        ds = [cnts_sort[j+1]-cnts_sort[j] for j in range(len(cnts)-1)]
        m = ds.index(max(ds))
        results[0], results[1] = cnts_sort[:m+1], cnts_sort[m+1:]
        ave0, ave1 = sum(results[0])/len(results[0]), sum(results[1])/len(results[1])
        for j in range(b):
            if abs(cnts[j]-ave0) < abs(cnts[j]-ave1):
                e_hint += "0"
            else:
                e_hint += "1"
                e0 += x^hint[j]

print(e0)

e1 = (bytes_to_poly(c)+e0)*h_inv%(x^n-1)
print(e1)

e = poly_to_bits(e0) + poly_to_bits(e1)
ss = c_buffer(int(ss_size))
res = libbike.crypto_kem_dec_from_e(ss, bytes(c), e)
print(bytes(ss).hex())

cipher = AES.new(key=bytes(ss), mode=AES.MODE_CTR, nonce=nonce)
flag = cipher.decrypt(enc_flag)
print(flag)
