# Root Cause

Every equation has its roots, and every root has its symmetry. Hmmm... do we need to multiply the roots to find out?

Author: AgileOrc

## Analysis

`chall.py`

```py
import random
from sympy import nextprime, isprime

BITS = 256
E = 65537
MOD_BITS = 26
NUM_PIECES = 11
EXPONENTS = [2, 3, 2]

def gen_roots():
    while True:
        rs = [random.randint(2**20, 2**30) for _ in range(2)]
        if len(set(rs)) == 2 and rs[0] % 2 == rs[1] % 2:
            return rs

def gen_k_and_primes(r1, r2):
    while True:
        start = random.getrandbits(BITS) | (1 << (BITS - 1))
        p1 = nextprime(start)
        k = p1 - r1
        if k <= 0:
            continue
        p2 = r2 + k
        if p1 == p2:
            continue
        if not isprime(p2):
            continue
        if (p1 - 1) % E == 0 or (p2 - 1) % E == 0:
            continue
        return k, p1, p2

def gen_extra_prime(bits=256):
    while True:
        cand = nextprime(random.getrandbits(bits) | (1 << (bits - 1)))
        if (cand - 1) % E != 0:
            return cand

def gen_moduli():
    moduli = []
    used = set()
    while len(moduli) < NUM_PIECES:
        cand = nextprime(random.getrandbits(MOD_BITS))
        if cand not in used:
            used.add(cand)
            moduli.append(cand)
    return moduli

def build_aux_pieces(k, moduli):
    pieces = []
    for m in moduli:
        leak = k % m
        decoy = random.randint(m + 1, m * 4)
        S = leak + decoy
        P = leak * decoy
        pieces.append({"m": m, "S": S, "P": P})
    return pieces

def main():
    r1, r2 = gen_roots()
    b = -(r1 + r2)
    c = r1 * r2

    k, p1, p2 = gen_k_and_primes(r1, r2)
    p3 = gen_extra_prime()

    moduli = gen_moduli()
    M = 1
    for m in moduli:
        M *= m
    assert M > k

    exponents = EXPONENTS.copy()
    random.shuffle(exponents)
    a1, a2, a3 = exponents
    N = (p1 ** a1) * (p2 ** a2) * (p3 ** a3)

    with open("flag.txt", "rb") as f:
        flag = f.read().strip()
    m_int = int.from_bytes(flag, "big")
    assert m_int < N
    enc_flag = pow(m_int, E, N)

    aux_pieces = build_aux_pieces(k, moduli)

    with open("output.txt", "w") as out:
        out.write(f"b = {b}\n")
        out.write(f"c = {c}\n")
        out.write(f"N = {N}\n")
        out.write(f"e = {E}\n")
        out.write(f"enc_flag = {enc_flag}\n")
        out.write(f"aux_pieces = {aux_pieces}\n")

if __name__ == "__main__":
    main()
```
```py
b = -407946574
c = 11628115226198413
N = 164103673186697727671722517410226002906879141982342298006270740993575128060288062377686357173615144650094900819078657436448212260441188396518435481548008982857808877755043040683468826834204148286862400745792942911835378554490970396965476874729956964887490530190715807606376876934079480979314518005127672139955529452398314934852303956344925712426471106427349767243505754306224918218253432291631725948044232476004787137247267688452041121917757041903922924197626084123090022652514946023212690698102436410479976971803282749892087676271910247477
e = 65537
enc_flag = 102832139856312140336726094268851743508377413685056466478748226207484626066630287716796833661909161899880937337618949062565552264033571851045993011107979073721293682863726166331594753684082828845118786778308204348436965601513817088775583392149401812385050290911191099259842128621204875936065554380892216940641331468951366485513574353970130737811703965209145155308271867280466084409254323109131133830508125204416074712106428838349225044881769804658631340533343501492660056186554271363488166023024317526226248126487617205847186710620133768946
aux_pieces = [{'m': 2561491, 'S': 11056512, 'P': 18053508979136}, {'m': 24608653, 'S': 86014386, 'P': 101242257423968}, {'m': 38948137, 'S': 58029350, 'P': 717480558864069}, {'m': 62359261, 'S': 285676679, 'P': 13019423790321208}, {'m': 54206773, 'S': 205805922, 'P': 2097964148493437}, {'m': 48192329, 'S': 209784813, 'P': 3352924911931992}, {'m': 18283693, 'S': 51673811, 'P': 20839805895774}, {'m': 65441393, 'S': 281422623, 'P': 7277550341099060}, {'m': 25730777, 'S': 41777697, 'P': 357141440780810}, {'m': 28848451, 'S': 61386549, 'P': 880081987210844}, {'m': 23598079, 'S': 94792540, 'P': 1363038669333891}]
```

RSA but with interesting math constraints like $N=p_1^{a_1}\cdot p_2^{a_2}\cdot p_3^{a_3}$ where exponents $(a_1,a_2,a_3)$ are shuffled set of $\{2,3,2\}$.

$r_1$ and $r_2$ are random 20-30 bits number. $b=-(r_1+r_2)$ and $c=r_1 \cdot r_2$, which is shown in the output. $b$ and $c$ also represent negated sum and product respectively (*Vieta's theorem*), so it's possible to form a quadratic equation to find roots $r_1$ and $r_2$.

$p_1$ is random 256-bit prime. $p_1 = r_1 + k$ to calculate $k$ then $p_2 = r_2 + k$, and $p_3$ is random 256-bit prime.

To find the 2 `p`'s, one needs to find `k`.

Code gives `k` through 11 clues (`aux_pieces`). For each random 26-bit prime moduli $m_i$:

- $leak_i = k \pmod{m_i}$. This means $leak_i < m_i$.
- $decoy_i = \text{randint(}m_i+1,m_i\cdot 4\text{)}$. This means $decoy_i > m_i$.
- $S_i=leak_i+decoy_i$
- $P_i=leak_i\cdot decoy_i$

$S$ and $P$ form another quadratic equation to be solved: $x^2 - Sx + P = 0$. It follows that $leak_i$ is the root $< m_i$, and $decoy_i$ is the root $> m_i$.

We only need $leak$ which forms the 11 small pieces of $k \pmod{m}$.

Then utilize *Chinese Remainder Theorem* to find $k$ using remainders and moduli. Calculate $p_1 = r_1 + k$ and $p_2 = r_2 + k$.

Bruteforce permutations of exponents $a_1, a_2, a_3$ to calculate $\large p_3^{a_3}=\frac{N}{p_1^{a_1}\cdot p_2^{a_2}}$ and find $p_3$, then find *Euler's totient*: $\phi(N) = p_1^{a_1-1}(p_1 - 1) \cdot p_2^{a_2-1}(p_2 - 1) \cdot p_3^{a_3-1}(p_3 - 1)$.

Find $d = e^{-1} \pmod{\phi(N)}$ and decrypt `enc_flag` like usual RSA.

## Sagemath Solution

```py
from sage.all import *
from itertools import *
from Crypto.Util.number import long_to_bytes
b = -407946574
c = 11628115226198413
N = 164103673186697727671722517410226002906879141982342298006270740993575128060288062377686357173615144650094900819078657436448212260441188396518435481548008982857808877755043040683468826834204148286862400745792942911835378554490970396965476874729956964887490530190715807606376876934079480979314518005127672139955529452398314934852303956344925712426471106427349767243505754306224918218253432291631725948044232476004787137247267688452041121917757041903922924197626084123090022652514946023212690698102436410479976971803282749892087676271910247477
e = 65537
enc_flag = 102832139856312140336726094268851743508377413685056466478748226207484626066630287716796833661909161899880937337618949062565552264033571851045993011107979073721293682863726166331594753684082828845118786778308204348436965601513817088775583392149401812385050290911191099259842128621204875936065554380892216940641331468951366485513574353970130737811703965209145155308271867280466084409254323109131133830508125204416074712106428838349225044881769804658631340533343501492660056186554271363488166023024317526226248126487617205847186710620133768946
aux_pieces = [{'m': 2561491, 'S': 11056512, 'P': 18053508979136}, {'m': 24608653, 'S': 86014386, 'P': 101242257423968}, {'m': 38948137, 'S': 58029350, 'P': 717480558864069}, {'m': 62359261, 'S': 285676679, 'P': 13019423790321208}, {'m': 54206773, 'S': 205805922, 'P': 2097964148493437}, {'m': 48192329, 'S': 209784813, 'P': 3352924911931992}, {'m': 18283693, 'S': 51673811, 'P': 20839805895774}, {'m': 65441393, 'S': 281422623, 'P': 7277550341099060}, {'m': 25730777, 'S': 41777697, 'P': 357141440780810}, {'m': 28848451, 'S': 61386549, 'P': 880081987210844}, {'m': 23598079, 'S': 94792540, 'P': 1363038669333891}]
rem = []
mod = []
Px = PolynomialRing(ZZ, 'x')
x = Px.gen()

# find leaks / k mod m
for bruh in aux_pieces:
    m,S,P = int(bruh['m']),int(bruh['S']),int(bruh['P'])
    f = x**2 - S*x + P
    roots = f.roots()
    root1 = roots[0][0]
    root2 = roots[1][0]
    if root1 < m:
        leak_candidate = root1
    else:
        leak_candidate = root2

    rem.append(leak_candidate)
    mod.append(m)

# crt
print(k:= crt(rem, mod))

# use public b & c for roots
Rt = PolynomialRing(ZZ, 't')
t = Rt.gen()
g = t**2 + b*t + c
rootss = g.roots()

# use roots and k to find p1 and p2
p1 = int(rootss[0][0])+ k
p2 = int(rootss[1][0]) + k

# bruteforce permutations to find p3
exponents = [2, 3, 2]
for a1, a2, a3 in set(permutations(exponents)):
    temp = Integer(N)
    if temp % (p1 ** a1) == 0:
        temp //= (p1 ** a1)
        if temp % (p2 ** a2) == 0:
            temp //= (p2 ** a2)
            p3_cand = temp.nth_root(a3)
            if p3_cand ** a3 == temp:
                print(f"{a1=}, {a2=}, {a3=}")
                exp1,exp2,exp3 = a1,a2,a3
                p3 = p3_cand
                break

# rsa decrypt
print('phi')
phi = (p1**(exp1-1)*(p1-1)) * (p2**(exp2-1) * (p2-1)) * (p3**(exp3-1) * (p3-1))
d = inverse_mod(e, phi)
mee= pow(enc_flag, d, N)
print(long_to_bytes(mee))
```
```sh
❯ python3 solve.py
101694372776216015433640492190357732373083760488654354886453535568463711485928
a1=2, a2=2, a3=3
phi
b'BeeCTF{wh3n_y0U_ne3D_b4S1C_4Lgebr4_t0_s0lv3_th1s_ch4lleng3_y4_beg1tul4H_p0k0kny4_ini_4ku_cum4N_m4U_m4njangin_fl4g_d04Ng_4w0KwaWokawkoawk}'
```

Flag: `BeeCTF{wh3n_y0U_ne3D_b4S1C_4Lgebr4_t0_s0lv3_th1s_ch4lleng3_y4_beg1tul4H_p0k0kny4_ini_4ku_cum4N_m4U_m4njangin_fl4g_d04Ng_4w0KwaWokawkoawk}`