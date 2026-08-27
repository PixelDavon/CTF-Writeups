from pwn import *

# Creates script in /tmp and run in SSH

sh = ssh('lotto', 'pwnable.kr', password='guest', port=2222)
p = sh.shell(tty=False)

remote_path = '/tmp/absolutecinemawow'
p.sendline(f'mkdir -p {remote_path}'.encode())

sh.upload('solve.py',f'{remote_path}/lotto.py')

p.sendline(f'python3 {remote_path}/lotto.py'.encode())
p.interactive()