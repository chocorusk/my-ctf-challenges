import os
import signal
from sage.misc.banner import require_version
from Crypto.Util.number import getPrime, bytes_to_long

assert require_version(10), "This challenge requires SageMath version 10 or above"

signal.alarm(30)
FLAG = os.environ.get("FLAG", "Alpaca{*** FAKEFLAG ***}").encode()
assert FLAG.startswith(b"Alpaca{")

p = getPrime(512)
q = getPrime(512)
n = p * q
e = 37

print("n:", n)
print("e:", e)

c = int(input("ciphertext: "))
assert 1 < c < n-1
pari.addprimes(p)
m = mod(c, n).nth_root(e)
print("plaintext:", m)

padded_flag = FLAG + os.urandom(127-len(FLAG))
print("encrypted flag:", pow(bytes_to_long(padded_flag), e, n))
