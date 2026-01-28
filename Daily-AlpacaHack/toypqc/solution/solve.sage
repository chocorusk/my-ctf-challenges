import ast

with open("../distfiles/output.txt") as f:
    A = ast.literal_eval(f.readline().lstrip("A = "))
    b = ast.literal_eval(f.readline().lstrip("b = "))

n = 7
m = 10
p = 8380417
F = GF(p)
A = matrix(F, A)
b = vector(F, b)

for e_bin in range(2**m):
    e = vector(F, [(e_bin>>i)&1 for i in range(m)])
    try:
        s = A.solve_right(b-e)
        flag = b"".join(int(s[i]).to_bytes(3, "big") for i in range(n))
        print(flag)
    except:
        continue