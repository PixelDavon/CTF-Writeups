Dump of assembler code for function main:
   0x08048671 <+0>:     push   ebp
   0x08048672 <+1>:     mov    ebp,esp
   0x08048674 <+3>:     push   ebx
   0x08048675 <+4>:     and    esp,0xfffffff0
   0x08048678 <+7>:     sub    esp,0x430
   0x0804867e <+13>:    mov    eax,DWORD PTR [ebp+0xc]
   0x08048681 <+16>:    mov    DWORD PTR [esp+0x1c],eax
   0x08048685 <+20>:    mov    eax,gs:0x14
   0x0804868b <+26>:    mov    DWORD PTR [esp+0x42c],eax
   0x08048692 <+33>:    xor    eax,eax
   0x08048694 <+35>:    mov    eax,ds:0x804a060
   0x08048699 <+40>:    mov    DWORD PTR [esp+0xc],0x0
   0x080486a1 <+48>:    mov    DWORD PTR [esp+0x8],0x2
   0x080486a9 <+56>:    mov    DWORD PTR [esp+0x4],0x0
   0x080486b1 <+64>:    mov    DWORD PTR [esp],eax
   0x080486b4 <+67>:    call   0x80484b0 <setvbuf@plt>
   0x080486b9 <+72>:    mov    eax,ds:0x804a040
   0x080486be <+77>:    mov    DWORD PTR [esp+0xc],0x0
   0x080486c6 <+85>:    mov    DWORD PTR [esp+0x8],0x1
   0x080486ce <+93>:    mov    DWORD PTR [esp+0x4],0x0
   0x080486d6 <+101>:   mov    DWORD PTR [esp],eax
   0x080486d9 <+104>:   call   0x80484b0 <setvbuf@plt>
   0x080486de <+109>:   mov    DWORD PTR ds:0x804a080,0x804a0a0
   0x080486e8 <+119>:   mov    DWORD PTR [esp],0x804890c
   0x080486ef <+126>:   call   0x8048470 <puts@plt>
   0x080486f4 <+131>:   mov    DWORD PTR [esp],0x8048934
   0x080486fb <+138>:   call   0x8048470 <puts@plt>
   0x08048700 <+143>:   mov    DWORD PTR [esp+0x8],0x400
   0x08048708 <+151>:   mov    DWORD PTR [esp+0x4],0x0
   0x08048710 <+159>:   lea    eax,[esp+0x2c]
   0x08048714 <+163>:   mov    DWORD PTR [esp],eax
   0x08048717 <+166>:   call   0x80484c0 <memset@plt>
   0x0804871c <+171>:   mov    eax,ds:0x804a040
   0x08048721 <+176>:   mov    DWORD PTR [esp+0x8],eax
   0x08048725 <+180>:   mov    DWORD PTR [esp+0x4],0x400
   0x0804872d <+188>:   lea    eax,[esp+0x2c]
   0x08048731 <+192>:   mov    DWORD PTR [esp],eax
   0x08048734 <+195>:   call   0x8048450 <fgets@plt>       ; input
   0x08048739 <+200>:   mov    DWORD PTR [esp+0x28],0x0
   0x08048741 <+208>:   jmp    0x8048760 <main+239>
   0x08048743 <+210>:   lea    edx,[esp+0x2c]
   0x08048747 <+214>:   mov    eax,DWORD PTR [esp+0x28]
   0x0804874b <+218>:   add    eax,edx
   0x0804874d <+220>:   movzx  eax,BYTE PTR [eax]
   0x08048750 <+223>:   movsx  eax,al
   0x08048753 <+226>:   mov    DWORD PTR [esp],eax
   0x08048756 <+229>:   call   0x80485dc <do_brainfuck>
   0x0804875b <+234>:   add    DWORD PTR [esp+0x28],0x1
   0x08048760 <+239>:   mov    ebx,DWORD PTR [esp+0x28]
   0x08048764 <+243>:   lea    eax,[esp+0x2c]
   0x08048768 <+247>:   mov    DWORD PTR [esp],eax
   0x0804876b <+250>:   call   0x8048490 <strlen@plt>
   0x08048770 <+255>:   cmp    ebx,eax
   0x08048772 <+257>:   jb     0x8048743 <main+210>
   0x08048774 <+259>:   mov    eax,0x0
   0x08048779 <+264>:   mov    edx,DWORD PTR [esp+0x42c]
   0x08048780 <+271>:   xor    edx,DWORD PTR gs:0x14
   0x08048787 <+278>:   je     0x804878e <main+285>
   0x08048789 <+280>:   call   0x8048460 <__stack_chk_fail@plt>
   0x0804878e <+285>:   mov    ebx,DWORD PTR [ebp-0x4]
   0x08048791 <+288>:   leave
   0x08048792 <+289>:   ret
End of assembler dump.