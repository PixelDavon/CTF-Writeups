# collision
## Analysis
```c
#include <stdio.h>
#include <string.h>
unsigned long hashcode = 0x21DD09EC;
unsigned long check_password(const char* p){
        int* ip = (int*)p;
        int i;
        int res=0;
        for(i=0; i<5; i++){
                res += ip[i];
        }
        return res;
}

int main(int argc, char* argv[]){
        if(argc<2){
                printf("usage : %s [passcode]\n", argv[0]);
                return 0;
        }
        if(strlen(argv[1]) != 20){
                printf("passcode length should be 20 bytes\n");
                return 0;
        }

        if(hashcode == check_password( argv[1] )){
                setregid(getegid(), getegid());
                system("/bin/cat flag");
                return 0;
        }
        else
                printf("wrong passcode.\n");
        return 0;
}
```
Code takes `argv[1]` (20 bytes), passes into `check_password()`, compares against `hashcode` to reveal flag.

`check_password` essentially takes a 20 bytes string, groups it into 5 "4 byte integer"s, adds all 5 big numbers into `res`.

>A short example is `AAAA` (4 bytes), stored as a `char` is `65 65 65 65` which is `01000001 01000001 01000001 01000001` in binary (0x41 0x41 0x41 0x41). This gets grouped together into 4 byte integer `01000001010000010100000101000001` (0x41414141) which is 1,094,795,585 in decimal.

If password is `AAAABBBBCCCCDDDDEEEE` then `res` is `1,094,795,585` + `1,111,638,594` + ...

## Solution

Divide `hashcode` (0x21DD09EC, 568,134,124 in decimal) into 5 groups.

$$
\begin{aligned}
\frac{568,134,124}{5}&=113,626,824 \text{ remainder }4 \\
&= 5 \times 113,626,824 + 4 \\
&= 113,626,824 + 113,626,824 + 113,626,824 + 113,626,824 + 113,626,824 + 4\ \\
&= 113,626,824 + 113,626,824 + 113,626,824 + 113,626,824 + 113,626,828
\end{aligned}
$$

113,626,824 = 0x6C5CEC8

113,626,828 = 0x6C5CECC

```py
from pwn import *

p = remote('pwnable.kr',10002)

passcode = 4*p32(0x6C5CEC8) + p32(0x6C5CECC)
print(passcode, len(passcode), type(passcode))

p.sendline(b'./col '+passcode)
p.interactive()
```
```shell
❯ python solve.py
[+] Opening connection to pwnable.kr on port 10002: Done
b'\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xcc\xce\xc5\x06' 20 <class 'bytes'>
[*] Switching to interactive mode
=====================================================================================
  [ Collision Shell ]
  Daddy told me about cool MD5 hash collision today
  I wanna do something like that too!

  ※ You got 500s in /bin/sh. Good luck.
  ※ Available: python2 python3 
=====================================================================================
Two_hash_collision_Nicely
$  
```

Flag: `Two_hash_collision_Nicely`