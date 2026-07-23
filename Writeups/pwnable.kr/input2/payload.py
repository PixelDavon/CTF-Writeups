# RUN ON PWNABLE.KR SERVER

from pwn import *
from os import pipe, write
# context.log_level='debug'
exe = b'./input2'             # argv 0

# exe = b'/home/input2/input2' (IF ON SSH)

args = [b'A'] * 100
args[65] = b'\x00'            # argv 65 (A)
args[66] = b'\x20\x0a\x0d'    # argv 66 (B)

PORT = 30472
args[67] = str(PORT).encode() # argv 67 (C)

stdin_read, stdin = pipe()
stderr_read, stderr = pipe()

write(stdin, b'\x00\x0a\x00\xff')
write(stderr, b'\x00\x0a\x02\xff')

env = {
    b'\xde\xad\xbe\xef': b'\xca\xfe\xba\xbe'
}

with open('\x0a','wb') as f:
    f.write(b'\x00\x00\x00\x00')

p = process(executable=exe, argv=args, stdin=stdin_read, stderr=stderr_read, env=env)
g = remote('localhost',PORT)
g.send(b'\xde\xad\xbe\xef')
g.close()

p.interactive()