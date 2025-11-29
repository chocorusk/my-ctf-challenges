import os
import random
from ctypes import cdll, c_buffer
from Crypto.Cipher import AES

with open("flag.txt", "rb") as f:
    FLAG = f.read()

libbike = cdll.LoadLibrary('./libbike.so')

libbike.randombytes_init(os.urandom(48), None, 256)

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
e_size = R_BYTES * N0

pk = c_buffer(pk_size)
sk = c_buffer(sk_size)
libbike.crypto_kem_keypair(pk, sk)
print("public key:", bytes(pk).hex())

ct = c_buffer(ct_size)
k_enc = c_buffer(ss_size)
e0 = c_buffer(R_BYTES)
libbike.crypto_kem_enc(ct, k_enc, e0, pk)
print("ciphertext:", bytes(ct).hex())

cipher = AES.new(key=bytes(k_enc), mode=AES.MODE_CTR)
encrypted_flag = cipher.encrypt(FLAG)
print("encrypted flag:", (cipher.nonce + encrypted_flag).hex())

e0_bin = "".join('{:08b}'.format(v)[::-1] for v in bytes(e0))[:n]

hint = [i for i in range(n) if e0_bin[i] == "1"] + random.sample([i for i in range(n) if e0_bin[i] == "0"], t - e0_bin.count("1"))
random.shuffle(hint)
e0_hint = "".join([e0_bin[i] for i in hint])
hint = hint[:16] + [(hint[i] + int(e0_hint[i-16:i], 2)) % n for i in range(16, len(hint))]
print("hint:", hint)

while True:
    ct_input = bytes.fromhex(input("ciphertext: "))
    assert len(ct_input) == ct_size
    k_dec = c_buffer(ss_size)
    res = libbike.crypto_kem_dec(k_dec, ct_input, sk)
    if res == 0:
        print("decapsulation succeed")
    else:
        print("decapsulation failed")
        continue
