with open("flag.txt", "r") as f:
    FLAG = f.read()

secret = randrange(2**256)

primes = []
p = secret
while len(primes) < 10:
    p = next_prime(p)
    primes.append(p)

for _ in range(50):
    a, b = map(int, input("a, b = ").split(","))
    if a == secret:
        print(FLAG)
        exit()
    if not (-2**31 <= a < 2**31 and -2**31 <= b < 2**31):
        exit(1)

    res = []
    for p in primes:
        R.<x> = PolynomialRing(GF(p))
        if (x^3+a*x+b).is_irreducible():
            res.append(p-secret)
    print(res)
