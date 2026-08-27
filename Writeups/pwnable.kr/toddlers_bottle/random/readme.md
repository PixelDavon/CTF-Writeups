# random
## Analysis
```c
#include <stdio.h>

int main(){
        unsigned int random;
        random = rand();        // random value!

        unsigned int key=0;
        scanf("%d", &key);

        if( (key ^ random) == 0xcafebabe ){
                printf("Good!\n");
                setregid(getegid(), getegid());
                system("/bin/cat flag");
                return 0;
        }

        printf("Wrong, maybe you should try 2^32 cases.\n");
        return 0;
}
```
If no `srand()` to set seed then default is `srand(1)`. Exact same sequence of numbers every run.

This means `rand()` is `1804289383`.

$$
\begin{aligned}
\text{key} \oplus \text{random} &= \text{0xcafebabe} \\
\text{key} \oplus \text{1804289383} &= \text{3405691582} \\
\text{key} &= \text{3405691582} \oplus \text{1804289383} \\
\text{key} &= 2708864985
\end{aligned}
$$

```sh
❯ nc pwnable.kr 10005
2708864985
Good!
m0mmy_I_can_predict_rand0m_v4lue!
```

Flag: `m0mmy_I_can_predict_rand0m_v4lue!`