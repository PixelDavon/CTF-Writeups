# brokentrustprotocol

**CTF:** Tracebash CTF

**Category:** crypto

**Difficulty:** 

**Tags:**

**Author:**

**Date:** June 2026

## Analysis
`protocol.py` encrypts flag by combining Diffie-Hellman Key Exchange with AES Symmetric Encryption. However, instead of $B=g^b \pmod{p}$ where $b$ is some secret random number, $B=p-1 \pmod{p}$, meaning:
$$
\begin{align*}
\text{shared} &= B^a \pmod{p}\\
\text{shared} &= (p-1)^a \pmod{p}\\
\text{shared}&\equiv (-1)^a \pmod{p}\\
\\
\text{if }a\text{ is even: } &\boxed{\text{shared} = 1 \pmod{p}}\\
\text{if }a\text{ is odd: } &\text{shared} = -1 \pmod{p}\\
&\boxed{\text{shared} = p-1 \pmod{p}}
\end{align*}
$$

Only 2 outputs are possible from `shared = pow(B,a,p)`. Since every other information is known, decryption is possible by just trying both `shared = 1 or p-1`.
## Solution
`solve.py`
```py
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from hashlib import sha256
from random import randint
import os
p = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031
g = 2
A = 803998869995081862638018864735364757357447752617850200720066936205676968588473376917853093289567968473807
B = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690030
iv = "fa919bb993a1befde685c90421595e27"
ciphertext = "534c708e7dd75a1b7ada5cb512d16bb2e8b6bf0df62b6f5e5df0e7e444fa46166426cb5a77d85b53032c3f959aeba907"
ct = bytes.fromhex(ciphertext)
iv = bytes.fromhex(iv)
possible_secrets = [1, p - 1]

for s in possible_secrets:
    key = sha256(str(s).encode()).digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        decrypted = unpad(cipher.decrypt(ct), 16)
        print(decrypted.decode())
    except:
        continue
```
Output
```
TBCTF{Sm4ll_Subgr0up_Att4cks_Ar3_D34dly}
```
<!-- ## Mitigation -->
<!-- Include if the challenge reflects a real-world vulnerability worth noting. -->

## Conclusion

Flag: `TBCTF{Sm4ll_Subgr0up_Att4cks_Ar3_D34dly}`