import os
from ptrlib import *
from Crypto.Cipher import ARC4
import string

chars = string.digits + string.ascii_lowercase + string.ascii_uppercase

sock = remote(os.environ.get("HOST", "localhost"), int(os.environ.get("PORT", 9999)))

def query(iv, ct = b'\x00'*256):
    sock.sendlineafter(b"iv: ", iv.hex())
    sock.sendlineafter(b"ciphertext: ", ct.hex())
    return bytes.fromhex(sock.recvlineafter("plaintext: ").strip().decode())

len_key = 16
master_key = ""
for k in range(len_key):
    iv = b'\x00'*(256-len_key-k-1)
    t = query(iv)
    for c in chars:
        iv = b'\x00'*(256-len_key-k-1) + (master_key+c).encode()
        s = query(iv)
        if s == t:
            master_key += c
            break
    print(master_key)

iv = b"\x00"
pt = master_key.encode()
ct = ARC4.new(master_key.encode() + iv, drop=3072).encrypt(pt)
sock.sendlineafter(b"iv: ", iv.hex())
sock.sendlineafter(b"ciphertext: ", ct.hex())
print(sock.recvline())
