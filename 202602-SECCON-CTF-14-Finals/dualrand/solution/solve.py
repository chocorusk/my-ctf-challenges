from z3 import *

# https://github.com/deut-erium/RNGeesus/blob/main/src/code_mersenne/mersenne.py
class MT19937:
    """
    Standard MT19937 instance for both 32 bit and 64 bit variants
    """
    def __init__(self, c_seed=0, bit_64=False):
        """
        initialize the mersenne twister with `c_seed`
        `bit_64` if True, would initialize the 64 variant of MT19937
        `c_seed` is 64-bit if `bit_64` set to True
        """
        # MT19937
        if bit_64:
            (self.w, n, self.m, self.r) = (64, 312, 156, 31)
            self.a = 0xB5026F5AA96619E9
            (self.u, self.d) = (29, 0x5555555555555555)
            (self.s, self.b) = (17, 0x71D67FFFEDA60000)
            (self.t, self.c) = (37, 0xFFF7EEE000000000)
            self.l = 43
            self.f = 6364136223846793005
        else:
            (self.w, n, self.m, self.r) = (32, 624, 397, 31)
            self.a = 0x9908B0DF
            (self.u, self.d) = (11, 0xFFFFFFFF)
            (self.s, self.b) = (7, 0x9D2C5680)
            (self.t, self.c) = (15, 0xEFC60000)
            self.l = 18
            self.f = 1812433253
        self.MT = [0 for i in range(n)]
        self.index = n + 1
        self.lower_mask = (1 << self.r) - 1  # 0x7FFFFFFF
        self.upper_mask = (1 << self.r)  # 0x80000000
        self.seed_mt(c_seed)

    def seed_mt(self, num):
        """initialize the generator from a seed"""
        self.MT[0] = num
        self.index = n
        for i in range(1, n):
            temp = self.f * (self.MT[i - 1] ^
                             (self.MT[i - 1] >> (self.w - 2))) + i
            self.MT[i] = temp & ((1 << self.w) - 1)

    def twist(self):
        """ Generate the next n values from the series x_i"""
        for i in range(0, n):
            x = (self.MT[i] & self.upper_mask) + \
                (self.MT[(i + 1) % n] & self.lower_mask)
            xA = x >> 1
            if (x % 2) != 0:
                xA = xA ^ self.a
            self.MT[i] = self.MT[(i + self.m) % n] ^ xA
        self.index = 0

    def extract_number(self):
        """
        extract tampered state at internal index i
        if index reaches end of state array, twist and set it to 0
        """
        if self.index >= n:
            self.twist()
        y = self.MT[self.index]
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)
        self.index += 1
        return y & ((1 << self.w) - 1)

    def get_state(self):
        """
        returning python compatible state
        """
        return (3, tuple(self.MT + [self.index]), None)


class MTpython(MT19937):
    """
    Additional functionality offered by MT of python3, namely 
    better (non linear) initialization 
    """
    def __init__(self, seed=0):
        MT19937.__init__(self, 0)
        self.seed(seed) #python seed initialization

    def init_by_array(self, init_key):
        """
        Initialization with an `init_key` array of 32-bit words for
        better randomization properties
        """
        self.seed_mt(19650218)
        i, j = 1, 0
        for k in range(max(n, len(init_key))):
            self.MT[i] = (self.MT[i] ^ (
                (self.MT[i - 1] ^ (self.MT[i - 1] >> 30)) * 1664525)) + init_key[j] + j
            self.MT[i] &= 0xffffffff
            i += 1
            j += 1
            if i >= n:
                self.MT[0] = self.MT[n - 1]
                i = 1
            if j >= len(init_key):
                j = 0
        for k in range(n - 1):
            self.MT[i] = (self.MT[i] ^ (
                (self.MT[i - 1] ^ (self.MT[i - 1] >> 30)) * 1566083941)) - i
            self.MT[i] &= 0xffffffff
            i += 1
            if i >= n:
                self.MT[0] = self.MT[n - 1]
                i = 1
        self.MT[0] = 0x80000000

    def init_32bit_seed(self, seed_32):
        """
        Just an oversimplification of `init_by_array` for single element array
        of upto 32 bit number
        """
        self.seed_mt(19650218)
        i = 1
        for k in range(n):
            self.MT[i] = (self.MT[i] ^ (
                (self.MT[i - 1] ^ (self.MT[i - 1] >> 30)) * 1664525)) + seed_32
            self.MT[i] &= 0xffffffff
            i += 1
            if i >= n:
                self.MT[0] = self.MT[n - 1]
                i = 1
        for k in range(n - 1):
            self.MT[i] = (self.MT[i] ^ (
                (self.MT[i - 1] ^ (self.MT[i - 1] >> 30)) * 1566083941)) - i
            self.MT[i] &= 0xffffffff
            i += 1
            if i >= n:
                self.MT[0] = self.MT[n - 1]
                i = 1
        self.MT[0] = 0x80000000

    def seed(self,seed_int):
        """
        Replication of random.seed of cpython when seed is an integer
        """
        self.init_by_array(self.int_to_array(seed_int))

    def random(self):
        """
        python random.random() call which yeilds a uniformly random
        floating point between [0,1] employing two MT 32 bits calls
        """
        a = self.extract_number()>>5
        b = self.extract_number()>>6
        return (a*67108864.0+b)*(1.0/9007199254740992.0)

    def int_to_array(self,k):
        """
        converting a big integer to equivalent list of 32-bit integers
        as would be passed into python seed process
        """
        if k==0:
            return [0]
        k_byte = int.to_bytes(k,(k.bit_length()+7)//8,'little')
        k_arr = [k_byte[i:i+4] for i in range(0,len(k_byte),4)]
        return [int.from_bytes(i,'little') for i in k_arr ]

    def array_to_int(self,arr):
        """
        converting list of 32-bit integers back to a big integer
        """
        arr_bytes  = b"".join([int.to_bytes(i,4,'little') for i in arr])
        return int.from_bytes( arr_bytes ,'little')

n = 624

# recover initial state

MT_init = MT19937(19650218).MT
MT = [BitVec(f'MT[{i}]', 32) for i in range(n)]
MT0 = BitVec(f'MT0', 32)
MT0 = MT[0]

lower_mask = 0x7FFFFFFF
upper_mask = 0x80000000
index = n
(w, n, m, r) = (32, 624, 397, 31)
a = 0x9908B0DF
(u, d) = (11, 0xFFFFFFFF)
(s, b) = (7, 0x9D2C5680)
(t, c) = (15, 0xEFC60000)
l = 18
f = 1812433253

N = 80
num_seeds = m - N + 1

OUTPUTS = [BitVec(f'output[{i}]', 32) for i in range(N)]

for _ in range(N):
    if index >= n:
        for i in range(n):
            x = (MT[i] & upper_mask) + \
                (MT[(i + 1) % n] & lower_mask)
            xA = LShR(x, 1)
            xA = If(x & 1 == 1, xA ^ a, xA)
            MT[i] = simplify(MT[(i + m) % n] ^ xA)
        index = 0
    y = MT[index]
    y = y ^ (LShR(y, u) & d)
    y = y ^ ((y << s) & b)
    y = y ^ ((y << t) & c)
    y = y ^ LShR(y, l)
    index += 1
    OUTPUTS[_] = y & ((1 << w) - 1)

S = Solver()
for i in range(N):
    S.add(OUTPUTS[i] == 0)
S.add(MT0 == 0x80000000)

print(S.check())
model = S.model()
recovered = { str(i):model[i].as_long() for i in model.decls() }
recovered = [ recovered[f'MT[{i}]'] if f"MT[{i}]" in recovered else 1 for i in range(n) ]
print(recovered)

# recover seed

MT = [BitVec(f'MT[{i}]', 32) for i in range(n)]
for i in range(n):
    MT[i] = BitVecVal(MT_init[i], 32)
SEEDS = [BitVec(f'seed[{i}]', 32) for i in range(num_seeds)]
i,j = 1,0
for k in range(n):
    MT[i] = (MT[i] ^ ((MT[i - 1] ^ LShR(MT[i - 1], 30)) * 1664525)) + SEEDS[j] + j
    MT[i] &= 0xffffffff
    i += 1
    j +=1
    if i >= n:
        MT[0] = MT[n - 1]
        i = 1
    if j == num_seeds:
        j=0
for k in range(n - 1):
    MT[i] = (MT[i] ^ ((MT[i - 1] ^ LShR(MT[i - 1], 30)) * 1566083941)) - i
    MT[i] &= 0xffffffff
    i += 1
    if i >= n:
        MT[0] = MT[n - 1]
        i = 1
MT[0] = BitVecVal(0x80000000, 32)

S = Solver()
for i in range(N+1):
    S.add(recovered[i] == MT[i])
for i in range(2*N-1, m-N):
    S.add(recovered[i] == MT[i])
for i in range(m, m+N):
    S.add(recovered[i] == MT[i])

print(S.check())
model = S.model()
recovered = { str(i):model[i].as_long() for i in model.decls() }
recovered = [ recovered[f'seed[{i}]'] for i in range(num_seeds) ]

M = MTpython()
seed = M.array_to_int(recovered)
print(seed)

import random
r = random.Random(seed)
print([r.randint(0, 0xdeedbeef) for _ in range(N)])

from ptrlib import *
sock = Socket("nc localhost 10395")
sock.sendlineafter("seed: ", str(seed))
ans = eval(sock.recvlineafter("hint:"))
sock.sendlineafter("answer: ", ",".join(map(str, ans)))
sock.interactive()
