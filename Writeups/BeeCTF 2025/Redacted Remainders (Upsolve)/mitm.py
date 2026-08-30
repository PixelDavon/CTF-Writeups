from Crypto.Util.number import inverse, long_to_bytes

n = 59213204637068816907517582537717244881250709490610600160235894584144862180589
e = 4099
c = 52598477212363693322221974252387327725937369173109674066499283883678096102095
dp_str = "1010 0010 0100 1111 1100 1101 r01r 0011 0101 r010 00r1 0r0r 11r0 0101 0r00 0001 rr01 1r01 1rr1 1r01 r1r1 rr01 01r1 001r 0r01 1111 1000 1011 1101 1110 1010 11"
dq_str = "1010 1110 0110 1001 1000 1011 0101 11rr 1000 0101 1100 110r 1r10 r110 0rr1 011r 110r rrr0 1r1r 01rr r110 1011 0rr1 1100 110r r1r0 1101 0001 0010 1001 1101 011"

def parse_masked_bits(masked: str):
   s = masked.replace(' ', '')
   L = len(s)
   base = 0
   unknown_pos = []
   for idx_msb, ch in enumerate(s):
       pos_lsb = L - 1 - idx_msb
       if ch == '0' or ch == '1':
           if ch == '1':
               base |= (1 << pos_lsb)
       else:
           unknown_pos.append(pos_lsb)
   return base, unknown_pos, L

def mitm_mod_subset(e, base, positions, k):
   mid = len(positions) // 2
   A = positions[:mid]
   B = positions[mid:]

   e_mod_k = e % k
   base_mod = (e_mod_k * (base % k) - 1) % k

   # All sums for A
   from collections import defaultdict
   table = defaultdict(list)
   LA = len(A)
   for mask in range(1 << LA):
       deltaA = 0
       sumA_mod = 0
       m = mask
       for i in range(LA):
           if m & 1:
               bit = A[i]
               deltaA += (1 << bit)
               sumA_mod = (sumA_mod + (e_mod_k * (1 << bit)) % k) % k
           m >>= 1
       table[sumA_mod].append(deltaA)

   LB = len(B)
   for mask in range(1 << LB):
       deltaB = 0
       sumB_mod = 0
       m = mask
       for i in range(LB):
           if m & 1:
               bit = B[i]
               deltaB += (1 << bit)
               sumB_mod = (sumB_mod + (e_mod_k * (1 << bit)) % k) % k
           m >>= 1
       need = (-base_mod - sumB_mod) % k
       if need in table:
           for deltaA in table[need]:
               yield deltaA + deltaB 

def try_recover_prime_from(masked_bits: str, n: int, e: int):
   base, unknown_positions, bitlen = parse_masked_bits(masked_bits)

   for k in range(1, e):
       print(f'\r{k=}\033[K',end='',flush=True)
       for delta in mitm_mod_subset(e, base, unknown_positions, k):
           dp_candidate = base + delta
           t = e * dp_candidate - 1
           if t % k != 0:
               continue
           p_candidate = 1 + t // k
           if p_candidate > 1 and n % p_candidate == 0:
               print(f'\n{k=} | {p_candidate=}')
               return int(p_candidate)
   return None

def solve():
   p = try_recover_prime_from(dp_str, n, e)
   if p is None:
       q_try = try_recover_prime_from(dq_str, n, e)
       if q_try is None:
           raise RuntimeError("Failed to recover a prime from dp and dq")
       q = q_try
       p = n // q
   else:
       q = n // p

   phi = (p - 1) * (q - 1)
   d = inverse(e, phi)
   m = pow(c, d, n)
   flag = long_to_bytes(m)
   return flag

if __name__ == "__main__":
   flag = solve()
   print(flag)