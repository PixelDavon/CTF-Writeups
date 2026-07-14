# statedesync

**CTF:** Tracebash CTF

**Category:** crypto

**Difficulty:** 

**Tags:**

**Author:** CYB3RFY

**Date:** June 2026

## Analysis
As mentioned in the comments in challenge code, the entire encryption relies on two 8-bit seeds `seed_a` and `seed_b`, which can only hold 256 possible states (0-255). Since whole encryption is XOR keystream, decryption is the same as encryption. Thus, bruteforce 256x256 = 65,536 possible seed combinations.

## Solution
Wrote solution directly in `challenge.py`:
```py
import binascii

# The flag was encrypted using this script with two secret 8-bit seeds.
# Can you recover it?

def custom_sbox(val):
    # A non-linear substitution AI won't have pre-computed tables for
    return ((val ^ 0x5A) + 0x33) % 256

# Previously was 'def encrypt'
def decrypt(data, seed_a, seed_b):
    state_a = seed_a
    state_b = seed_b
    ciphertext = bytearray()
    
    for byte in data:
        # Irregular clocking: Inner loop length dynamically changes
        clock_steps = (state_a & 0x0F) + 1 
        for _ in range(clock_steps):
            # Custom bitwise shift
            feedback = ((state_b >> 7) ^ (state_b >> 5) ^ (state_b >> 2) ^ (state_b >> 1)) & 1
            state_b = ((state_b << 1) | feedback) & 0xFF
            
        state_a = custom_sbox(state_a ^ state_b)
        
        keystream_byte = custom_sbox(state_b) ^ state_a
        ciphertext.append(byte ^ keystream_byte)
        
    return ciphertext


# SOLUTION
ciphertext = binascii.unhexlify("1ad9756e666a336be1388c7d132c0a83aecfb9735366374196e187f78e38ece6")

for seed_a in range(256):
    for seed_b in range(256):
        pt = decrypt(ciphertext, seed_a, seed_b)
        try:
            pt_str = pt.decode('ascii')
            if "TBCTF{" in pt_str.lower() or "{" in pt_str.lower():
                print(f"[!] Keys found: seed_a = {seed_a}, seed_b = {seed_b}")
                print(f"[!] Recovered Flag: {pt_str}")
                exit(0)
        except UnicodeDecodeError:
            # cant be decoded as ASCII
            continue
```
Output
```
[!] Keys found: seed_a = 66, seed_b = 19
[!] Recovered Flag: TBCTF{h1dd3n_st4t3_m4chin3_f4il}
```
<!-- ## Mitigation -->
<!-- Include if the challenge reflects a real-world vulnerability worth noting. -->

## Conclusion

Flag: `TBCTF{h1dd3n_st4t3_m4chin3_f4il}`