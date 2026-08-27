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