Dump of assembler code for function do_brainfuck:
   0x080485dc <+0>:     push   ebp
   0x080485dd <+1>:     mov    ebp,esp
   0x080485df <+3>:     push   ebx
   0x080485e0 <+4>:     sub    esp,0x24
   0x080485e3 <+7>:     mov    eax,DWORD PTR [ebp+0x8]
   0x080485e6 <+10>:    mov    BYTE PTR [ebp-0xc],al
   0x080485e9 <+13>:    movsx  eax,BYTE PTR [ebp-0xc]
   0x080485ed <+17>:    sub    eax,0x2b
   0x080485f0 <+20>:    cmp    eax,0x30
   0x080485f3 <+23>:    ja     0x804866b <do_brainfuck+143>
   0x080485f5 <+25>:    mov    eax,DWORD PTR [eax*4+0x8048848]
   0x080485fc <+32>:    jmp    eax
   0x080485fe <+34>:    mov    eax,ds:0x804a080
   0x08048603 <+39>:    add    eax,0x1
   0x08048606 <+42>:    mov    ds:0x804a080,eax
   0x0804860b <+47>:    jmp    0x804866b <do_brainfuck+143>
   0x0804860d <+49>:    mov    eax,ds:0x804a080
   0x08048612 <+54>:    sub    eax,0x1
   0x08048615 <+57>:    mov    ds:0x804a080,eax
   0x0804861a <+62>:    jmp    0x804866b <do_brainfuck+143>
   0x0804861c <+64>:    mov    eax,ds:0x804a080
   0x08048621 <+69>:    movzx  edx,BYTE PTR [eax]
   0x08048624 <+72>:    add    edx,0x1
   0x08048627 <+75>:    mov    BYTE PTR [eax],dl
   0x08048629 <+77>:    jmp    0x804866b <do_brainfuck+143>
   0x0804862b <+79>:    mov    eax,ds:0x804a080
   0x08048630 <+84>:    movzx  edx,BYTE PTR [eax]
   0x08048633 <+87>:    sub    edx,0x1
   0x08048636 <+90>:    mov    BYTE PTR [eax],dl
   0x08048638 <+92>:    jmp    0x804866b <do_brainfuck+143>
   0x0804863a <+94>:    mov    eax,ds:0x804a080
   0x0804863f <+99>:    movzx  eax,BYTE PTR [eax]
   0x08048642 <+102>:   movsx  eax,al
   0x08048645 <+105>:   mov    DWORD PTR [esp],eax
   0x08048648 <+108>:   call   0x80484d0 <putchar@plt>
   0x0804864d <+113>:   jmp    0x804866b <do_brainfuck+143>
   0x0804864f <+115>:   mov    ebx,DWORD PTR ds:0x804a080
   0x08048655 <+121>:   call   0x8048440 <getchar@plt>
   0x0804865a <+126>:   mov    BYTE PTR [ebx],al
   0x0804865c <+128>:   jmp    0x804866b <do_brainfuck+143>
   0x0804865e <+130>:   mov    DWORD PTR [esp],0x8048830
   0x08048665 <+137>:   call   0x8048470 <puts@plt>
   0x0804866a <+142>:   nop
   0x0804866b <+143>:   add    esp,0x24
   0x0804866e <+146>:   pop    ebx
   0x0804866f <+147>:   pop    ebp
   0x08048670 <+148>:   ret
End of assembler dump.