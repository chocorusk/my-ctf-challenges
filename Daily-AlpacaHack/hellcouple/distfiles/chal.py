import secrets
import hashlib
from Crypto.Cipher import AES
import os

FLAG = os.getenv("FLAG", "Alpaca{dummy}").encode()

# https://datatracker.ietf.org/doc/html/rfc3526#section-2
p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g = 2

alice_private = secrets.randbelow(p)
bob_private = secrets.randbelow(p)

alice_public = pow(g, alice_private, p)
bob_public = pow(g, bob_private, p)

print("alice_public:", alice_public)
print("bob_public:", bob_public)
print("leak:", alice_private & (2**1500 - 1))

shared_key = pow(alice_public, bob_private, p)
assert shared_key == pow(bob_public, alice_private, p)
session_key = hashlib.sha256(shared_key.to_bytes(p.bit_length() // 8, "big")).digest()

cipher = AES.new(session_key, AES.MODE_CTR)
encrypted_flag = cipher.nonce + cipher.encrypt(FLAG)
print("encrypted_flag:", encrypted_flag.hex())
