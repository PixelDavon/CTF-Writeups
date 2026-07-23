# coin1

## Analysis
```sh
coin1@ubuntu:~$ nc 0 10009

        ---------------------------------------------------
        -              Shall we play a game?              -
        ---------------------------------------------------

        You have given some gold coins in your hand
        however, there is one counterfeit coin among them
        counterfeit coin looks exactly same as real coin
        however, its weight is different from real one
        real coin weighs 10, counterfeit coin weighes 9
        help me to find the counterfeit coin with a scale
        if you find 100 counterfeit coins, you will get reward :)
        FYI, you have 60 seconds.

        - How to play -
        1. you get a number of coins (N) and number of chances (C)
        2. then you specify a set of index numbers of coins to be weighed
        3. you get the weight information
        4. 2~3 repeats C time, then you give the answer

        - Example -
        [Server] N=4 C=2        # find counterfeit among 4 coins with 2 trial
        [Client] 0 1            # weigh first and second coin
        [Server] 20                     # scale result : 20
        [Client] 3                      # weigh fourth coin
        [Server] 10                     # scale result : 10
        [Client] 2                      # counterfeit coin is third!
        [Server] Correct!

        - Ready? starting in 3 sec... -

N=6 C=3
```
1 counterfeit (9kg) in `N` coins (each real coin 10kg). For `C` times, we are able to know the weight of whichever coins we want by their indexes.

Finding 1 specific target element in a whole array should remind you of binary search.

### Modified Binary Search

```py
R = real, C = counterfeit
l = left pointer, r = right pointer

l    mid    r
R  R  C  R  R
0  1  2  3  4

weight (l, mid) coins = 10+10+9 = 29

l    mid
R  R  C
0  1  2

if all 3 coins are REAL then weight is 3*10 = 30 
but weight != 30, meaning counterfeit is inside scope.

so lower scope by setting r = mid

l mid r
R  R  C
0  1  2

weight (l, mid) coins = 20
the 2 coins are REAL, so focus outside the (l, mid) scope by setting l = mid + 1

      l
      r
R  R  C
0  1  2

l == r, so coin index 2 is COUNTERFEIT.
```

Basically weight (l, mid) coins. If counterfeit is inside the scope (compare weight to predicted weight as if all coins are real), then lower `r` to `mid`, otherwise raise `l` to `mid + 1`.

## Solution

Implement the binary search in python:
`payload.py`

```py
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
```

Since directly connecting to `pwnable.kr` results in significant network latency, it's better to run the script on the ssh server itself.

`solve.py`

```py
from pwn import *
# context.log_level='debug'

with open('payload.py','rb') as f:
    payload = f.read()

sh = ssh(user='coin1',host='pwnable.kr',password='guest',port=2222)
p = sh.shell(tty=False)

remote_path = '/tmp/absolute_cinema'

p.sendline(f'mkdir -p {remote_path}'.encode())
sh.upload('./payload.py', f'{remote_path}/test.py')

p.sendline(f'python3 {remote_path}/test.py'.encode())

p.interactive()
```
```sh
❯ python3 solve.py
[+] Connecting to pwnable.kr on port 2222: Done
[*] coin1@pwnable.kr:
    Distro    Ubuntu 22.04
    OS:       linux
    Arch:     amd64
    Version:  5.15.0
    ASLR:     Enabled
    SHSTK:    Disabled
    IBT:      Disabled
[+] Opening new channel: 'shell': Done
[*] Uploading './payload.py' to '/tmp/absolute_cinema/test.py'
[*] Switching to interactive mode
Warning: _curses.error: setupterm: could not find terminfo database

Terminal features will not be available.  Consider setting TERM variable to your current terminal name (or xterm).
[x] Opening connection to localhost on port 10009
[x] Opening connection to localhost on port 10009: Trying 127.0.0.1
[+] Opening connection to localhost on port 10009: Done
[*] Switching to interactive mode
9
Correct! (99)
Congrats! get your flag
b1naRy_S34rch1Ng_1s_3asy_p3asy
```

Flag: `b1naRy_S34rch1Ng_1s_3asy_p3asy`