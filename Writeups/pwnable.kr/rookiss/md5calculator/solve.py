from pwn import *

sh = ssh('md5calculator', 'pwnable.kr', port=2222, password='guest')

folder = '/tmp/absolutecinema'
remote_script = f'{folder}/test.py'

sh.system(f'mkdir -p {folder}')
sh.upload_file('./payload.py', remote_script)

p = sh.process(['python3', remote_script])
p.interactive()