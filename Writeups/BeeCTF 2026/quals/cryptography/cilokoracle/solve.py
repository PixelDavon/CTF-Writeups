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