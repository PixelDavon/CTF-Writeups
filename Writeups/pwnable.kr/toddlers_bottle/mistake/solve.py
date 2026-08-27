from pwn import *

p = remote('pwnable.kr',10008)

pw = b'bruhbruh67'

p.sendline(pw)
p.recvuntil(b'input password :')
p.sendline(b''.join(chr(x^1).encode() for x in pw))

p.interactive()
