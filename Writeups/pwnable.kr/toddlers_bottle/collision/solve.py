from pwn import *

p = remote('pwnable.kr',10002)

passcode = 4*p32(0x6C5CEC8) + p32(0x6C5CECC)
print(passcode, len(passcode), type(passcode))

p.sendline(b'./col '+passcode)
p.interactive()