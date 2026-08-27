# Flux Capacitor

The Flux Capacitor in Dr. Brown's old car is acting up, leaving him stuck in the wrong timeline. Maybe the “data” inside it can help him get the DeLorean running again.

Author: c0smic

## Analysis

We are given

```sh
❯ exiftool chall
ExifTool Version Number         : 12.40
File Name                       : chall
Directory                       : .
File Size                       : 32 KiB
File Modification Date/Time     : 2026:08:23 16:32:38+07:00
File Access Date/Time           : 2026:08:23 16:32:38+07:00
File Inode Change Date/Time     : 2026:08:23 16:32:38+07:00
File Permissions                : -rwxrwxrwx
File Type                       : ELF shared library
File Type Extension             : so
MIME Type                       : application/octet-stream
CPU Architecture                : 64 bit
CPU Byte Order                  : Little endian
Object File Type                : Shared object file
CPU Type                        : AMD x86-64
```

I tried running it but

```sh
❯ ./chall
./chall: /lib/x86_64-linux-gnu/libc.so.6: version `GLIBC_2.38' not found (required by ./chall)
```

So I had to install `glib-all-in-one` and patch the ELF:

```sh
patchelf --set-interpreter ~/DevTools/glibc-all-in-one/libs/2.38-1ubuntu6.3_amd64/x86_64-linux-gnu/ld-linux-x86-64.so.2 chall
patchelf --set-rpath ~/DevTools/glibc-all-in-one/libs/2.38-1ubuntu6.3_amd64/x86_64-linux-gnu/ chall
```

Anyways

```sh
❯ ./chall
[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
[][]                                                    [][]
[][]  FLUX CAPACITOR TEMPORAL CALIBRATION SYSTEM v1.21  [][]
[][]                                                    [][]
[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]

Enter your calibration note:
1
How many bytes of memory state do you want to inspect?
1
Inspecting 1 bytes from Flux Memory:
49, 

Enter the 64-bit Flux Hash to initiate Time Travel:
1

Temporal Hash Mismatch! You are stuck in 1955!
```

Opening it in Ghidra gives the overall gist: (I renamed some local vars)

```c
undefined8 main(void)

{
  undefined8 uVar1;
  char *pcVar2;
  char hash_input_buf [32];
  char inspect_len_buf [16];
  char note_buf [79];
  byte key_byte;
  ulong expected_hash;
  ulong user_hash;
  uint inspect_bytes_count;
  char *heap_buf;
  long j;
  long i;
  
  FUN_001011e9();
  setvbuf(stdout,(char *)0x0,2,0);
  heap_buf = calloc(0xfa,1);
  if (heap_buf == (char *)0x0) {
    uVar1 = 1;
  }
  else {
    for (i = 0; (&DAT_00102030)[i] != '\0'; i = i + 1) {
      heap_buf[i + 0xbe] = (&DAT_00102030)[i] ^ 0x6a;
    }
    puts("[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]");
    puts("[][]                                                    [][]");
    puts("[][]  FLUX CAPACITOR TEMPORAL CALIBRATION SYSTEM v1.21  [][]");
    puts("[][]                                                    [][]");
    puts("[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]");
    puts("");
    puts("Enter your calibration note:");
    pcVar2 = fgets(note_buf,0x40,stdin);
    if (pcVar2 == (char *)0x0) {
      uVar1 = 1;
    }
    else if (note_buf[0] == '\n') {
      puts("Critical Error");
      uVar1 = 0;
    }
    else {
      strncpy(heap_buf,note_buf,0x30);
      puts("How many bytes of memory state do you want to inspect?");
      pcVar2 = fgets(inspect_len_buf,0x10,stdin);
      if (pcVar2 == (char *)0x0) {
        uVar1 = 1;
      }
      else if (inspect_len_buf[0] == '\n') {
        puts("Critical Error");
        uVar1 = 0;
      }
      else {
        inspect_bytes_count = atoi(inspect_len_buf);
        printf("Inspecting %d bytes from Flux Memory:\n",(ulong)inspect_bytes_count);
        inspect_mem(heap_buf,(long)(int)inspect_bytes_count);
        puts("\nEnter the 64-bit Flux Hash to initiate Time Travel:");
        pcVar2 = fgets(hash_input_buf,0x20,stdin);
        if (pcVar2 == (char *)0x0) {
          uVar1 = 1;
        }
        else if (hash_input_buf[0] == '\n') {
          puts("Critical Error");
          uVar1 = 0;
        }
        else {
          user_hash = __isoc23_strtoull(hash_input_buf,0,10);
          expected_hash = compute_flux_hash(heap_buf + 0xbe);
          if ((user_hash == expected_hash) && (user_hash != 0)) {
            puts("\n1.21 GIGAWATTS ACHIEVED!");
            puts("Temporal Displacement Initialized! Great Scott!");
            for (j = 0; (&DAT_00102060)[j] != '\0'; j = j + 1) {
              key_byte = (byte)(user_hash >> (sbyte)(((uint)j & 7) << 3));
              putchar((uint)((&DAT_00102060)[j] ^ key_byte));
            }
            putchar(10);
          }
          else {
            puts("\nTemporal Hash Mismatch! You are stuck in 1955!");
          }
          free(heap_buf);
          uVar1 = 0;
        }
      }
    }
  }
  return uVar1;
}
```

To get flag, `user_hash == expected_hash`, and `expected_hash = compute_flux_hash(heap_buf + 0xbe);`.

We can find out what's inside `heap_buf + 0xbe (190 in decimal)` by inspecting memory from the second prompt:

```c
puts("How many bytes of memory state do you want to inspect?");
...
inspect_bytes_count = atoi(inspect_len_buf);
printf("Inspecting %d bytes from Flux Memory:\n",(ulong)inspect_bytes_count);
inspect_mem(heap_buf,(long)(int)inspect_bytes_count);
```

But there's a catch in the function:

```c
void inspect_mem(long buffer,ulong length)

{
  ulong curr_byte;
  int i;
  
  for (i = 0; (ulong)(long)i < length; i = i + 1) {
    curr_byte = (ulong)*(char *)(buffer + i);
    if ((0xbd < i) && (i < 0xda)) {
      curr_byte = (long)(i % 7 + 0x37) ^ curr_byte; // XORed
    }
    printf("%llu, ",curr_byte);
  }
  putchar(10);
  return;
}
```

If `189 < i < 218`, byte is XORed with `(i % 7 + 0x37)`. But that's easily reversable.

Looking further

```c
puts("\nEnter the 64-bit Flux Hash to initiate Time Travel:");
pcVar2 = fgets(hash_input_buf,0x20,stdin);
...
user_hash = __isoc23_strtoull(hash_input_buf,0,10);
expected_hash = compute_flux_hash(heap_buf + 0xbe);
if ((user_hash == expected_hash) && (user_hash != 0)) {
```

So, we know something special is in index 190-217 of `heap_buf`, since `heap_buf + 190` is used to compute the flux hash.

```c
ulong compute_flux_hash(byte *str_ptr)

{
  ulong uVar1;
  byte *curr_ptr;
  long char_idx;
  ulong hash_val;
  
  hash_val = 0x1505;
  char_idx = 0;
  curr_ptr = str_ptr;
  while( true ) {
    if (*curr_ptr == 0) break;
    uVar1 = (long)(int)(uint)*curr_ptr + hash_val * 0x21;
    hash_val = uVar1 ^ uVar1 >> 0xd ^ char_idx * -0x61c8864680b583eb;
    char_idx = char_idx + 1;
    curr_ptr = curr_ptr + 1;
  }
  return hash_val;
}
```

Not too complicated to replicate in Python, though bitmasking is necessary to simulate 64-bit integer overflow since we're working with unsigned long long.

## Solution

```py
from pwn import *
p = process('./chall')
mask = (1 << 64) - 1
gggg = 0x9E3779B97F4A7C15 # 2^64 - 0x61c8864680b583eb
def flux_hash(data:bytes) -> int:
    h = 0x1505
    for i, b in enumerate(data):
        val = (b + h * 0x21) & mask
        h = (val ^ (val >> 0xd) ^ ((i * gggg) & mask)) & mask
    return h

p.recvuntil(b'calibration note:\n')
p.sendline(b'A')
p.recvuntil(b'inspect?\n')
p.sendline(b'218')

p.recvuntil(b'Flux Memory:\n')
line = p.recvline().strip().decode()
values = [int(x) for x in line.rstrip(',').split(', ') if x]

encoded = []
for i in range(190, 218):
    printed = values[i]
    raw = printed ^ ((i % 7) + 0x37)
    if raw == 0:
        break
    encoded.append(raw)

secret_bytes = bytes(encoded)
h = flux_hash(secret_bytes)
log.info(f" {secret_bytes}")
log.info(f"{h}")
p.recvuntil(b'Time Travel:\n')
p.sendline(str(h).encode())
print(p.recvall().decode())
```

```sh
❯ python3 solve.py
[+] Starting local process './chall': pid 44411
[*]  b'p3ng3n_PunY4_d3l0r34n_1985'
[*] 7150136296559265265
[+] Receiving all data: Done (126B)
[*] Process './chall' stopped with exit code 0 (pid 44411)

1.21 GIGAWATTS ACHIEVED!
Temporal Displacement Initialized! Great Scott!
BeeCTF{flUx_cApAc1t0r_d3crYpt3d_sUcc3ss_djb21s34sy}
```

Flag: `BeeCTF{flUx_cApAc1t0r_d3crYpt3d_sUcc3ss_djb21s34sy}`