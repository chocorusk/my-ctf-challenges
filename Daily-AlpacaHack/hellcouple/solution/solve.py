import hashlib
from Crypto.Cipher import AES
import math

with open("../distfiles/output.txt") as f:
    alice_public = int(f.readline().split(":")[1])
    bob_public = int(f.readline().split(":")[1])
    leak = int(f.readline().split(":")[1])
    encrypted_flag = bytes.fromhex(f.readline().split(":")[1])

def bsgs(g, h, p, bound):
    d = int(math.sqrt(bound))
    pow_dict = dict()
    gp = 1
    for i in range(d):
        pow_dict[gp] = i
        gp = gp*g%p
    gd = pow(g, -d, p)
    h1 = h
    for i in range(0, bound, d):
        if h1 in pow_dict:
            return i + pow_dict[h1]
        h1 = h1*gd%p
    return -1

p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g = 2
h = pow(g, 2**1500, p)
A = alice_public * pow(g, -leak, p) % p
a = bsgs(h, A, p, 2**36)
alice_private = a*(2**1500)+leak

shared_key = pow(bob_public, alice_private, p)
session_key = hashlib.sha256(shared_key.to_bytes(p.bit_length() // 8, "big")).digest()

cipher = AES.new(session_key, AES.MODE_CTR, nonce=encrypted_flag[:8])
flag = cipher.decrypt(encrypted_flag[8:])
print(flag)
