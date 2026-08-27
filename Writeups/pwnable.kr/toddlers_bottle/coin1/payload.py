# RUN ON PWNABLE.KR SSH SERVER

from pwn import *
import re

# context.log_level='debug'

p = remote('localhost',10009)
p.recvuntil(b'- Ready? starting in 3 sec... -')

def guess():
    line = p.recvuntil(b'N=') and p.recvline()
    N,C = [int(num) for num in re.findall(r'\d+', line.decode())]

    l,r = 0,N-1

    for _ in range(C):
        if l==r:
            p.sendline(b'%d' % l)
            continue
        mid = (l+r)//2
        p.sendline(' '.join(map(str,range(l,mid+1))).encode())
        weight = int(p.recvline())

        if weight != 10*(mid-l+1):
            r=mid
        else:
            l=mid+1
    return r

for i in range(100):
    g = guess()
    p.sendline(b'%d' % g)

p.interactive()