with open("../distfiles/output.txt") as f:
    encrypted_msg = bytes.fromhex(f.readline().split(":")[1])
    encrypted_flag = bytes.fromhex(f.readline().split(":")[1])

def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

msg = b"Daily AlpacaHack is a daily CTF challenge with a fun new puzzle every day."
keystream = xor(encrypted_msg, msg)
print(xor(encrypted_flag, keystream))
