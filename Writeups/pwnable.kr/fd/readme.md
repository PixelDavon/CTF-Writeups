# fd
## Analyze
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char buf[32];
int main(int argc, char* argv[], char* envp[]){
        if(argc<2){
                printf("pass argv[1] a number\n");
                return 0;
        }
        int fd = atoi( argv[1] ) - 0x1234;
        int len = 0;
        len = read(fd, buf, 32);
        if(!strcmp("LETMEWIN\n", buf)){
                printf("good job :)\n");
                setregid(getegid(), getegid());
                system("/bin/cat flag");
                exit(0);
        }
        printf("learn about Linux file IO\n");
        return 0;

}
```
Takes first argument, turns it into number, subtracts by 0x1234 (4660), passed into first argument of `read()`.

`read(int fd, void *buf, size_t count)` arguments in C:
1. **int fd**: File Descriptor, int assigned by OS for a stream. Standard input = 0, Standard output = 1, Standard error = 2. `fd` is usually obtained from `open()` which returns non-negative (& non-reserved) integers which is $\ge3$.
2. **void \*buf**: Buffer Pointer to memory location. Data reads from `fd` and stored in `buf`.
3. **size_t count**: Max Byte Count to read from `fd` into `buf`. *should never exceed allocated size of buffer otherwise memory corruption / buffer overflows*.
4. `read()` ideally returns the specific number of bytes it read from `fd` into `buf`.

```c
len = read(fd, buf, 32);
if(!strcmp("LETMEWIN\n", buf)){
    ...
    system("/bin/cat flag");
    ...
}
```
`strcmp` returns `0` if both strings are identical, which is why negation `!` is necessary.

Code means read 32 bytes from `fd` into `buf`. Compare `buf` to `LETMEWIN\n`. If `!0`->`true`, print flag.

## Solution

Ideally, we want `standard input` (`0`) to be our `fd` so we could type into the buffer.
```c
int fd = atoi( argv[1] ) - 0x1234;
int len = 0;
len = read(fd, buf, 32);
```
Since `fd` is `first arg - 4660`, then our `first argument` to the program is `4660`.
```
fd@ubuntu:~$ ./fd 4660
LETMEWIN
good job :)
Mama! Now_I_understand_what_file_descriptors_are!
fd@ubuntu:~$ ./fd 4661
LETMEWIN
good job :)
Mama! Now_I_understand_what_file_descriptors_are!
fd@ubuntu:~$ ./fd 4662
LETMEWIN
good job :)
Mama! Now_I_understand_what_file_descriptors_are!
fd@ubuntu:~$ ./fd 4663
learn about Linux file IO
fd@ubuntu:~$
```
Interestingly, all file descriptors (stdin, stdout, and stderr) works because they all READ from the same exact terminal keyboard input queue.

**Flag**: `Mama! Now_I_understand_what_file_descriptors_are!`