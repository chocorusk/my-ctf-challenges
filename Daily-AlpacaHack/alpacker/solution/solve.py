import subprocess

with open("../distfiles/chal", "rb") as f:
    f.seek(0x3020)
    bin = f.read(0x11b)

bin = [v * 0x73 % 256 for v in bin]

with open("check", "wb") as f:
    f.write(bytes(bin))

# objdump -D -b binary -mi386 -M intel check
res = subprocess.check_output(["objdump", "-D", "-b", "binary", "-mi386", "-M", "intel", "check"]).decode()

flag = [0]*36
for line in res.split("\n"):
    if "cmp" not in line:
        continue
    if "+" not in line:
        idx = 0
    else:
        idx = int(line.split("+")[1].split("]")[0], 16)
    val = int(line.split(",")[1], 16)
    flag[idx] = val
print(bytes(flag))
