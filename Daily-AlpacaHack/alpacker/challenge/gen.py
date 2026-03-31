import random
import subprocess

flag = b"Alpaca{kaw4ii_min1419aca_1n_4lp4ca!}"

asm = '''BITS 64
global check

check:
\txor\teax, eax

'''

idx = list(range(len(flag)))
random.shuffle(idx)

for i in idx:
    asm += f"\tcmp\tbyte [rdi+{i}], {hex(flag[i])}\n"
    asm += f"\tjne\t.ret\n"

asm += '''
\tmov\t eax, 1
.ret:
\tret
'''

with open("check.asm", "w") as f:
    f.write(asm)

subprocess.run(["nasm", "check.asm"])

with open("check", "rb") as f:
    bin = f.read()
    print([v * pow(0x73, -1, 256) % 256 for v in bin])
