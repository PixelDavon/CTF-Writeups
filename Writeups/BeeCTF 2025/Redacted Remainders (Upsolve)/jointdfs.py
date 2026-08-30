from Crypto.Util.number import inverse, long_to_bytes

n = 59213204637068816907517582537717244881250709490610600160235894584144862180589
e = 4099
c = 52598477212363693322221974252387327725937369173109674066499283883678096102095
dp_str = "1010 0010 0100 1111 1100 1101 r01r 0011 0101 r010 00r1 0r0r 11r0 0101 0r00 0001 rr01 1r01 1rr1 1r01 r1r1 rr01 01r1 001r 0r01 1111 1000 1011 1101 1110 1010 11"
dq_str = "1010 1110 0110 1001 1000 1011 0101 11rr 1000 0101 1100 110r 1r10 r110 0rr1 011r 110r rrr0 1r1r 01rr r110 1011 0rr1 1100 110r r1r0 1101 0001 0010 1001 1101 011"

def get_char_at_bit(bit_string, bit_idx):
    """Safely fetch the bit character at position `bit_idx` (0 = LSB).
    If we ask for a bit beyond the string length, it's implicitly '0'."""
    str_idx = len(bit_string) - 1 - bit_idx
    if str_idx < 0:
        return '0'
    return bit_string[str_idx]

def solve_rsa(n, e, c, dp_str, dq_str):
    # 1. Strip spaces in strings
    dp_str = dp_str.replace(" ", "")
    dq_str = dq_str.replace(" ", "")

    # 2. Min/Max boundaries for the missing bits
    dp_min = int(dp_str.replace('r', '0'), 2)
    dp_max = int(dp_str.replace('r', '1'), 2)
    
    dq_min = int(dq_str.replace('r', '0'), 2)
    dq_max = int(dq_str.replace('r', '1'), 2)

    # 3. Calculate Product Window with the safety bounds
    min_prod = max(1, (e**2 * dp_min * dq_min) // n - 2)
    max_prod = (e**2 * dp_max * dq_max) // n + 3

    print(f"[*] Targeting kp*kq product range: [{min_prod}, {max_prod}]")

    # 4. Search for valid (kp, kq) pairs
    candidates = []
    for kp in range(1, e):
        for target_prod in range(min_prod, max_prod + 1):
            if target_prod % kp == 0:
                kq = target_prod // kp
                if 1 <= kq < e:
                    candidates.append((kp, kq))

    # Remove dupes
    candidates = list(set(candidates))
    print(f"[*] Found {len(candidates)} candidate (kp, kq) pairs.")

    # 5. Joint-DFS
    for kp, kq in candidates:
        # states hold: (p_val, q_val)
        states = [(1, 1)] 
        
        # p and q are exactly 128 bits long
        for i in range(1, 128):
            if not states:
                break 
            
            next_states = []
            mod_mask = (1 << (i + 1))
            e_inv = inverse(e, mod_mask)
            
            for p_val, q_val in states:
                for p_i in (0, 1):
                    p_cand = p_val | (p_i << i)
                    
                    # Constraint 1: Modulus N (Forces q_i)
                    q_i = ((n - p_cand * q_val) >> i) & 1
                    q_cand = q_val | (q_i << i)
                    
                    if (p_cand * q_cand) % mod_mask != n % mod_mask:
                        continue
                        
                    # Constraint 2: Oracle Check
                    dp_cand = (e_inv * (kp * (p_cand - 1) + 1)) % mod_mask
                    dq_cand = (e_inv * (kq * (q_cand - 1) + 1)) % mod_mask
                    
                    dp_bit = (dp_cand >> i) & 1
                    dq_bit = (dq_cand >> i) & 1
                    
                    # Constraint 3: Compare against masked strings safely
                    dp_char = get_char_at_bit(dp_str, i)
                    dq_char = get_char_at_bit(dq_str, i)
                    
                    dp_match = (dp_char == 'r') or (int(dp_char) == dp_bit)
                    dq_match = (dq_char == 'r') or (int(dq_char) == dq_bit)
                    
                    if dp_match and dq_match:
                        next_states.append((p_cand, q_cand))
                        
            states = next_states
        
        # 6. Verify p and q
        for p_final, q_final in states:
            if p_final * q_final == n:
                print(f"[+] Factored N")
                print(f"[+] p: {p_final}")
                print(f"[+] q: {q_final}")
                print(f"[+] {kp=} {kq=}")
                
                phi = (p_final - 1) * (q_final - 1)
                d = inverse(e, phi)
                m = pow(c, d, n)
                print(f"\n[+] Flag: {long_to_bytes(m).decode(errors='ignore')}")
                return

    print("[-] DFS exhausted. No valid factors found.")

solve_rsa(n, e, c, dp_str, dq_str)