#!/usr/bin/env python3

import random

r1 = random.SystemRandom()
r2 = random.Random(int(input('seed: ')))

ans = [r1.randint(0, 0xdeadbeef) for _ in range(80)]
key = [r2.randint(0, 0xdeadbeef) for _ in range(80)]
r1.shuffle(key)

print("hint:", [a ^ b for a, b in zip(ans, key)])
if list(map(int, input('answer: ').split(','))) == ans:
    print("flag:", open("flag.txt", "r").read())
else:
    print("nope.")