# Cilok-Oracle

Jujur aja, Mang Dadang udah capek jualan cilok ditawar terus. Biar keliatan eksklusif kayak startup, dia sok-sokan nge-enkripsi resep rahasianya pake AES. Masalahnya, dia males baca dokumentasi. Tiap lu nitip adonan lu sendiri, resep aslinya malah kegeser dan kecetak jelas polanya di blok sebelahnya.

Author: kyr0

## Analysis

```sh
❯ nc 103.185.52.197 3254

=== Warung Cilok Oracle ===
1. Titip bumbu tambahan
2. Minta resep rahasia
3. Pulang
> 1
bumbu (hex): 01
cilok: 04b937f8c272554539f905da8ff2b561ef1ea3be1b6b264dc0bb6acedbc49d1a02f07282b80d2478cf925f1bc3bef88c3db5e3befc390759f799a845436c97d0146ea546dce134ca451410880379b69e

=== Warung Cilok Oracle ===
1. Titip bumbu tambahan
2. Minta resep rahasia
3. Pulang
> 1
bumbu (hex): 01
cilok: 04b937f8c272554539f905da8ff2b561ef1ea3be1b6b264dc0bb6acedbc49d1a02f07282b80d2478cf925f1bc3bef88c3db5e3befc390759f799a845436c97d0146ea546dce134ca451410880379b69e

=== Warung Cilok Oracle ===
1. Titip bumbu tambahan
2. Minta resep rahasia
3. Pulang
> 1
bumbu (hex): 02
cilok: a9a27b3f37ec9e5b327ffafc0739f319ef1ea3be1b6b264dc0bb6acedbc49d1a02f07282b80d2478cf925f1bc3bef88c3db5e3befc390759f799a845436c97d0146ea546dce134ca451410880379b69e

=== Warung Cilok Oracle ===
1. Titip bumbu tambahan
2. Minta resep rahasia
3. Pulang
> 3
Makasih sudah mampir.
```

AES uses 16-byte blocks. By observation, the same `bumbu` results in the same `cilok` (*which implies no IV/nonce*), and notice:

```sh
bumbu = 1: 04b937f8c272554539f905da8ff2b561 | ef1ea3be1b6b264dc0bb6acedbc49d1a 
bumbu = 2: a9a27b3f37ec9e5b327ffafc0739f319 | ef1ea3be1b6b264dc0bb6acedbc49d1a
```

This means 16-byte chunks are encrypted *independently* which is the flaw of *AES-ECB*. Thus, this challenge is a **Byte at a Time ECB Decryption Attack** (or **ECB Chosen-Plaintext Attack**).

The setup is `[inputted padding] + [flag]`. (since first block changed with different `bumbu`).

### The idea (Example)

Isolate and bruteforce last byte in 16-byte block.

```
Given unknown flag is BeeCTF{abcdefghijklmnopqrstuvwxyz}.

Send 15 bytes of padding "A"
Server: AES( AAAAAAAAAAAAAAAB | eeCTF... )

We know target first block hash: AES( AAAAAAAAAAAAAAAB ).
The first 15*A from our input and "B" from the server.
We don't know "B" is the correct char.

We find the correct char by bruteforcing 1 byte after padding:
AAAAAAAAAAAAAAAa
AAAAAAAAAAAAAAAb
AAAAAAAAAAAAAAAc
...
AAAAAAAAAAAAAAAB -> Server encrypts and gives AES( AAAAAAAAAAAAAAAB | BeeCTF... )

First block hash from our bruteforce == target first block hash. We add correct char "B" to our result.

Then send 14*A and take note of first block:
AES( 14*A + 1 known flag byte + 1 new unknown byte ). Bruteforce unknown byte.

Repeat with decreasing padding, bruteforcing last byte, and accumulating flag bytes.

For first block, it ends at bruteforcing "BeeCTF{abcdefgh?" -> "BeeCTF{abcdefghi" (16 characters)

For second block, send 15*A to get AES( 15*A+B | eeCTF{abcdefghij | kl... )
Second block is AES( 15 known flag + 1 unknown ). Pattern follows.
```

## Solution

```py
from pwn import *
BS = 16
p = remote("103.185.52.197", 3254)
def oracle(x):
    p.sendlineafter(b"> ", b"1")
    p.sendlineafter(b"bumbu (hex): ", x.hex().encode())
    p.recvuntil(b"cilok: ")
    return bytes.fromhex(p.recvline().strip().decode())


def block(ct,n):
    return ct[n*BS : (n+1)*BS]


flag = b""
alp = b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-{}"
while not flag.endswith(b'}'):
    i = len(flag)
    pad_len = BS-1-(i%BS)
    pad = b"A" * pad_len

    blockk = i//BS

    t_ct = oracle(pad)
    t = block(t_ct, blockk)

    pref = pad + flag

    found = False
    for c in alp:
        pr = pref + bytes([c])
        cand = oracle(pr)

        if block(cand, blockk) == t:
            flag += bytes([c])

            log.success(
                f"[{i:02d}] {chr(c)!r} -> "
                f"{flag.decode(errors='replace')}"
            )

            found = True
            break
    if not found:
        log.failure(f"FAILED byte {i}")
        log.info(f"block i  {blockk}")
        log.info(f"target  {t.hex()}")
        break
print()
log.success(f"flag fr {flag.decode(errors='replace')}")
p.close()
```
```sh
❯ python3 solve.py
[+] Opening connection to 103.185.52.197 on port 3254: Done
[+] [00] 'B' -> B
[+] [01] 'E' -> BE
[+] [02] 'E' -> BEE
[+] [03] 'C' -> BEEC
[+] [04] 'T' -> BEECT
[+] [05] 'F' -> BEECTF
[+] [06] '{' -> BEECTF{
[+] [07] 'n' -> BEECTF{n
[+] [08] 'y' -> BEECTF{ny
[+] [09] '1' -> BEECTF{ny1
[+] [10] 'c' -> BEECTF{ny1c
[+] [11] '1' -> BEECTF{ny1c1
[+] [12] 'l' -> BEECTF{ny1c1l
[+] [13] '_' -> BEECTF{ny1c1l_
[+] [14] 's' -> BEECTF{ny1c1l_s
[+] [15] '4' -> BEECTF{ny1c1l_s4
[+] [16] 't' -> BEECTF{ny1c1l_s4t
[+] [17] 'u' -> BEECTF{ny1c1l_s4tu
[+] [18] '_' -> BEECTF{ny1c1l_s4tu_
[+] [19] 'b' -> BEECTF{ny1c1l_s4tu_b
[+] [20] 'y' -> BEECTF{ny1c1l_s4tu_by
[+] [21] 't' -> BEECTF{ny1c1l_s4tu_byt
[+] [22] '3' -> BEECTF{ny1c1l_s4tu_byt3
[+] [23] '_' -> BEECTF{ny1c1l_s4tu_byt3_
[+] [24] 'p' -> BEECTF{ny1c1l_s4tu_byt3_p
[+] [25] '3' -> BEECTF{ny1c1l_s4tu_byt3_p3
[+] [26] 'r' -> BEECTF{ny1c1l_s4tu_byt3_p3r
[+] [27] '_' -> BEECTF{ny1c1l_s4tu_byt3_p3r_
[+] [28] 's' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s
[+] [29] '4' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4
[+] [30] 't' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4t
[+] [31] 'u' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu
[+] [32] '_' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_
[+] [33] 'b' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_b
[+] [34] 'y' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_by
[+] [35] 't' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt
[+] [36] '3' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3
[+] [37] '_' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_
[+] [38] 'k' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k
[+] [39] '4' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4
[+] [40] 'y' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y
[+] [41] '4' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4
[+] [42] 'k' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k
[+] [43] '_' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_
[+] [44] 'n' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_n
[+] [45] 'y' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny
[+] [46] '1' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1
[+] [47] 'c' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c
[+] [48] '1' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1
[+] [49] 'l' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l
[+] [50] '_' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_
[+] [51] 'p' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p
[+] [52] '1' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1
[+] [53] 'n' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1n
[+] [54] 'j' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1nj
[+] [55] '0' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1nj0
[+] [56] 'l' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1nj0l
[+] [57] '_' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1nj0l_
[+] [58] 'y' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1nj0l_y
[+] [59] '4' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1nj0l_y4
[+] [60] '_' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1nj0l_y4_
[+] [61] 'b' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1nj0l_y4_b
[+] [62] '4' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1nj0l_y4_b4
[+] [63] 'n' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1nj0l_y4_b4n
[+] [64] '9' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1nj0l_y4_b4n9
[+] [65] '_' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1nj0l_y4_b4n9_
[+] [66] '7' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1nj0l_y4_b4n9_7
[+] [67] 'a' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1nj0l_y4_b4n9_7a
[+] [68] '9' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1nj0l_y4_b4n9_7a9
[+] [69] 'f' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1nj0l_y4_b4n9_7a9f
[+] [70] '2' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1nj0l_y4_b4n9_7a9f2
[+] [71] 'c' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1nj0l_y4_b4n9_7a9f2c
[+] [72] '1' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1nj0l_y4_b4n9_7a9f2c1
[+] [73] 'b' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1nj0l_y4_b4n9_7a9f2c1b
[+] [74] '}' -> BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1nj0l_y4_b4n9_7a9f2c1b}

[+] flag fr BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1nj0l_y4_b4n9_7a9f2c1b}
[*] Closed connection to 103.185.52.197 port 3254
```

Flag: `BEECTF{ny1c1l_s4tu_byt3_p3r_s4tu_byt3_k4y4k_ny1c1l_p1nj0l_y4_b4n9_7a9f2c1b}`