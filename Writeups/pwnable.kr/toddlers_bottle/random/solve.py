from pwn import *
p = remote('pwnable.kr',10005)
p.sendline(b'2708864985')
p.interactive()