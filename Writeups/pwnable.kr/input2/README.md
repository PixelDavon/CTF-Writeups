# input2
## Analysis
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>

int main(int argc, char* argv[], char* envp[]){
        printf("Welcome to pwnable.kr\n");
        printf("Let's see if you know how to give input to program\n");
        printf("Just give me correct inputs then you will get the flag :)\n");

        // argv
        if(argc != 100) return 0;
        if(strcmp(argv['A'],"\x00")) return 0;
        if(strcmp(argv['B'],"\x20\x0a\x0d")) return 0;
        printf("Stage 1 clear!\n");

        // stdio
        char buf[4];
        read(0, buf, 4);
        if(memcmp(buf, "\x00\x0a\x00\xff", 4)) return 0;
        read(2, buf, 4);
        if(memcmp(buf, "\x00\x0a\x02\xff", 4)) return 0;
        printf("Stage 2 clear!\n");

        // env
        if(strcmp("\xca\xfe\xba\xbe", getenv("\xde\xad\xbe\xef"))) return 0;
        printf("Stage 3 clear!\n");

        // file
        FILE* fp = fopen("\x0a", "r");
        if(!fp) return 0;
        if( fread(buf, 4, 1, fp)!=1 ) return 0;
        if( memcmp(buf, "\x00\x00\x00\x00", 4) ) return 0;
        fclose(fp);
        printf("Stage 4 clear!\n");

        // network
        int sd, cd;
        struct sockaddr_in saddr, caddr;
        sd = socket(AF_INET, SOCK_STREAM, 0);
        if(sd == -1){
                printf("socket error, tell admin\n");
                return 0;
        }
        saddr.sin_family = AF_INET;
        saddr.sin_addr.s_addr = INADDR_ANY;
        saddr.sin_port = htons( atoi(argv['C']) );
        if(bind(sd, (struct sockaddr*)&saddr, sizeof(saddr)) < 0){
                printf("bind error, use another port\n");
                return 1;
        }
        listen(sd, 1);
        int c = sizeof(struct sockaddr_in);
        cd = accept(sd, (struct sockaddr *)&caddr, (socklen_t*)&c);
        if(cd < 0){
                printf("accept error, tell admin\n");
                return 0;
        }
        if( recv(cd, buf, 4, 0) != 4 ) return 0;
        if(memcmp(buf, "\xde\xad\xbe\xef", 4)) return 0;
        printf("Stage 5 clear!\n");

        // here's your flag
        setregid(getegid(), getegid());
        system("/bin/cat flag");
        return 0;
}
```
Use `pwntools` because `process()` provides useful arguments specifically for the first 3 stages, such as `executable`, `argv`, `stdin` & `stderr` pipe, and `env` for environment variables. The rest is simple python.

### Stage 1

```c
if(argc != 100) return 0;
if(strcmp(argv['A'],"\x00")) return 0;
if(strcmp(argv['B'],"\x20\x0a\x0d")) return 0;
```

This stage requires argument length to be 100. `argv['A']` is implicitly treated as `argv[65]` (ascii value of A). Same goes with `argv['B']`. Both argv needs to be `\x00` and `\x20\x0a\x0d` respectively.

```py
exe = b'./input2'

args = [b'A'] * 100
args[65] = b'\x00'
args[66] = b'\x20\x0a\x0d'
```

### Stage 2
```c
char buf[4];
read(0, buf, 4);
if(memcmp(buf, "\x00\x0a\x00\xff", 4)) return 0;
read(2, buf, 4);
if(memcmp(buf, "\x00\x0a\x02\xff", 4)) return 0;
printf("Stage 2 clear!\n");
```
This reads from `stdin` and `stderr` stream. We can do

```py
process(stdin=*read pipe*, stderr=*another read pipe*)
```
We use `os.pipe()` to create pipe and write into pipe.
```py
stdin_read, stdin = pipe()
stderr_read, stderr = pipe()

write(stdin, b'\x00\x0a\x00\xff')
write(stderr, b'\x00\x0a\x02\xff')
```

### Stage 3
```c
if(strcmp("\xca\xfe\xba\xbe", getenv("\xde\xad\xbe\xef"))) return 0;
printf("Stage 3 clear!\n");
```

`process()` has `env` argument that accepts a dictionary.
```py
env = {
    b'\xde\xad\xbe\xef': b'\xca\xfe\xba\xbe'
}
```

### Stage 4

```c
FILE* fp = fopen("\x0a", "r");
if(!fp) return 0;
if( fread(buf, 4, 1, fp)!=1 ) return 0;
if( memcmp(buf, "\x00\x00\x00\x00", 4) ) return 0;
fclose(fp);
printf("Stage 4 clear!\n");
```

This requires a file named `\x0a` (newline) with contents `\x00\x00\x00\x00`.

```py
with open('\x0a','wb') as f:
    f.write(b'\x00\x00\x00\x00')
```

### Stage 5

```c
int sd, cd;
struct sockaddr_in saddr, caddr;
sd = socket(AF_INET, SOCK_STREAM, 0);
if(sd == -1){
        printf("socket error, tell admin\n");
        return 0;
}
saddr.sin_family = AF_INET;
saddr.sin_addr.s_addr = INADDR_ANY;
saddr.sin_port = htons( atoi(argv['C']) );
if(bind(sd, (struct sockaddr*)&saddr, sizeof(saddr)) < 0){
        printf("bind error, use another port\n");
        return 1;
}
listen(sd, 1);
int c = sizeof(struct sockaddr_in);
cd = accept(sd, (struct sockaddr *)&caddr, (socklen_t*)&c);
if(cd < 0){
        printf("accept error, tell admin\n");
        return 0;
}
if( recv(cd, buf, 4, 0) != 4 ) return 0;
if(memcmp(buf, "\xde\xad\xbe\xef", 4)) return 0;
printf("Stage 5 clear!\n");
```
Since the payload is going to be run in `pwnable.kr` server, use another `remote()` (or python socket alternatively) to connect to localhost and send `\xde\xad\xbe\xef`.
```py
g = remote('localhost',PORT)
g.send(b'\xde\xad\xbe\xef')
g.close()
```

## Solution

Combine all approach (consider the order)

`payload.py`

```py
# RUN ON PWNABLE.KR SERVER

from pwn import *
from os import pipe, write
# context.log_level='debug'
exe = b'./input2'             # argv 0

# exe = b'/home/input2/input2' (IF ON SSH)

args = [b'A'] * 100
args[65] = b'\x00'            # argv 65 (A)
args[66] = b'\x20\x0a\x0d'    # argv 66 (B)

PORT = 30472 # random port
args[67] = str(PORT).encode() # argv 67 (C)

stdin_read, stdin = pipe()
stderr_read, stderr = pipe()

write(stdin, b'\x00\x0a\x00\xff')
write(stderr, b'\x00\x0a\x02\xff')

env = {
    b'\xde\xad\xbe\xef': b'\xca\xfe\xba\xbe'
}

with open('\x0a','wb') as f:
    f.write(b'\x00\x00\x00\x00')

p = process(executable=exe, argv=args, stdin=stdin_read, stderr=stderr_read, env=env)
g = remote('localhost',PORT)
g.send(b'\xde\xad\xbe\xef')
g.close()

p.interactive()
```

`solve.py`

```py
from pwn import *

p = remote('pwnable.kr',10006)

with open('payload.py','rb') as f:
    payload=f.read()

p.sendline(b'cat <<"EOF">test.py')
p.sendline(payload)
p.sendline(b'EOF')
p.sendline(b'python3 test.py')

p.interactive()
```
Output
```shell
❯ python3 solve.py
[+] Opening connection to pwnable.kr on port 10006: Done
[*] Switching to interactive mode
=====================================================================================
  [ Input2 Shell ]
  Mom? how can I pass my input to a computer program?

  ※ You got 500s in /bin/sh. Good luck.
  ※ Available: python2 python3 pwntools 
=====================================================================================
Warning: _curses.error: setupterm: could not find terminfo database

Terminal features will not be available.  Consider setting TERM variable to your current terminal name (or xterm).
[x] Starting local process './input2'
[+] Starting local process './input2': pid 1441
[x] Opening connection to localhost on port 30472
[x] Opening connection to localhost on port 30472: Trying ::1
[x] Opening connection to localhost on port 30472: Trying 127.0.0.1
[+] Opening connection to localhost on port 30472: Done
[*] Closed connection to localhost port 30472
[*] Switching to interactive mode
Welcome to pwnable.kr
Let's see if you know how to give input to program
Just give me correct inputs then you will get the flag :)
Stage 1 clear!
Stage 2 clear!
Stage 3 clear!
Stage 4 clear!
Stage 5 clear!
Mommy_now_I_know_how_to_pa5s_inputs_in_Linux
[*] Process './input2' stopped with exit code 0 (pid 1441)
[*] Got EOF while reading in interactive
$  
```

Flag: `Mommy_now_I_know_how_to_pa5s_inputs_in_Linux`