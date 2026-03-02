# You can run this file localy like following command
# socat TCP-L:1337,fork,reuseaddr EXEC:'python3 ./server.py' 
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
from Crypto.Util.Padding import pad, unpad
import os
import string
import random
from conn import client
import signal

def encrypt(pt, e, n):
    m = bytes_to_long(pad(pt, 16))
    assert m < n
    ct = pow(m, e, n)
    return ct


def decrypt(ct, d, n):
    m = pow(ct, d, n)
    pt = unpad(long_to_bytes(m), 16)
    return pt

def main():
    FLAG = os.environ.get("FLAG", "SECCON{dummy_flag}")
    secret = "SECCON{" + "".join(random.choices(string.ascii_letters, k=0x37)) + "}"

    nbit = 1024
    e = 65537

    while True:
        p = getPrime(nbit // 2)
        q = getPrime(nbit // 2)
        n = p * q
        if n >= 2 ** (nbit - 1) and (p - 1) * (q - 1) % e != 0:
            break

    print("n:", n)
    d = pow(e, -1, (p - 1) * (q - 1))

    ct = encrypt(secret.encode(), e, n)
    print("encrypted secret:", ct)

    query_count = 0
    while True:
        inp = input("ciphertext or guess: ")
        if inp == secret:
            return 0x37 / (query_count+1) * 10000
        query_count += 1
        ct = int(inp)
        try:
            decrypt(ct, d, n)
            print("success")
        except Exception as e:
            print("error:", e)


if __name__ == "__main__":
    signal.alarm(60*5)
    team_id = input("team_id> ")
    client(main, team_id)
