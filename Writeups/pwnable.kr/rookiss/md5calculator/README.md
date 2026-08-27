# md5 calculator

```sh
Arch:       i386-32-little
RELRO:      Partial RELRO
Stack:      Canary found
NX:         NX enabled
PIE:        No PIE (0x8048000)
Stripped:   No
```

## A few observations

```c
int my_hash(void)
{
  int iVar1;
  int in_GS_OFFSET;
  int local_3c;
  int local_30 [4];
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int canary;
  
  canary = *(int *)(in_GS_OFFSET + 0x14);
  for (local_3c = 0; local_3c < 8; local_3c = local_3c + 1) {
    iVar1 = rand();
    local_30[local_3c] = iVar1;
  }
  if (canary != *(int *)(in_GS_OFFSET + 0x14)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return local_1c + local_30[1] + (local_30[2] - local_30[3]) + canary + local_14 +
         (local_20 - local_18);
}
```

Canary value is used as part of captcha. 8 Rands with `srand(time(0))` into an array. It's viable to run both program and `rand` locally for the same sequences of random numbers.

Analyze in `gdb` for accurate offsets.

$$
\text{(local) \quad srand(time(0));} \quad \text{For }i=0\text{ to 7: arr[i]}=\text{rand()} 
\\
\text{Captcha} = \text{arr[1]}+\text{arr[5]}+\text{arr[2]}-\text{arr[3]}+\text{arr[7]}+\text{Canary}+\text{arr[4]}-\text{arr[6]}
\\
\text{Captcha} = \text{idxs sum} + \text{Canary}
\\
\text{(Receive captcha)}
\\
\text{Canary} = \text{Captcha} - \text{idxs sum}
$$

Canary value is known so BOF is possible even with Stack Canary.

Imagine:

```nasm
Buffer
            (Few last bytes of buffer)       (Canary, ending in 00)
0xffffc350: 0xdeadbeef  0xdeadbeef  0xdeadbeef  0x670ddf00
            (Saved Reg) (Saved Reg) (Saved EBP) (Return Addr)
0xffffc360: 0xf7cab000  0xf7ffcb80  0xffffc398  0x08049174

Then, knowing the Canary, payload could be: A*12 + Canary + A*12 + Another Address
```
If `Another Address` is a `call` then it pushes ret addr and saved EBP to stack, sets EBP = ESP at beginning.