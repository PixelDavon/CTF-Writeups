from pwn import *

p = remote('pwnable.kr',10007)

p.recvuntil(b'/ $')
p.sendline(b'./leg')
p.sendline(b'108400')

p.interactive()