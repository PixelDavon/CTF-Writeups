from pwn import *
p = process('./chall')
mask = (1 << 64) - 1
gggg = 0x9E3779B97F4A7C15 # 2^64 - 0x61c8864680b583eb
def flux_hash(data:bytes) -> int:
    h = 0x1505
    for i, b in enumerate(data):
        val = (b + h * 0x21) & mask
        h = (val ^ (val >> 0xd) ^ ((i * gggg) & mask)) & mask
    return h

p.recvuntil(b'calibration note:\n')
p.sendline(b'A')
p.recvuntil(b'inspect?\n')
p.sendline(b'218')

p.recvuntil(b'Flux Memory:\n')
line = p.recvline().strip().decode()
values = [int(x) for x in line.rstrip(',').split(', ') if x]

encoded = []
for i in range(190, 218):
    printed = values[i]
    raw = printed ^ ((i % 7) + 0x37)
    if raw == 0:
        break
    encoded.append(raw)

secret_bytes = bytes(encoded)
h = flux_hash(secret_bytes)
log.info(f" {secret_bytes}")
log.info(f"{h}")
p.recvuntil(b'Time Travel:\n')
p.sendline(str(h).encode())
print(p.recvall().decode())