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