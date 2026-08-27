#!/usr/bin/env python3

from pwn import *
import re
# context.log_level='debug'
p = remote('pwnable.kr',10014)

for i in range(10):
  line = p.recvuntil(b'specify the memcpy amount between') and p.recvuntil(b':')
  low,high = [int(x) for x in re.findall(r'\d+', line.decode())]
  mid = (low+high)//2
  chunk = mid+8
  if 1 <= (chunk % 16) <= 8 and chunk<=high:
    mid+=8

  p.sendline(b'%d' % mid)

p.interactive()