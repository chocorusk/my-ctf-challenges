from Crypto.Cipher import ChaCha20
import os

FLAG = os.getenv("FLAG", "Alpaca{dummy}").encode()

key = os.urandom(32)
nonce = os.urandom(8)

def encrypt(plaintext):
    cipher = ChaCha20.new(key=key, nonce=nonce)
    return cipher.encrypt(plaintext)

msg = b"Daily AlpacaHack is a daily CTF challenge with a fun new puzzle every day."
print("encrypted msg:", encrypt(msg).hex())
print("encrypted flag:", encrypt(FLAG).hex())
