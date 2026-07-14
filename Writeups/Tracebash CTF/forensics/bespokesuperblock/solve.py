corrupted = b'tbctf[SPAT\x11AL\x7fAWARE\x7fXOR\x7f\x11\x13\x13\x17]'
flag = bytes(b ^ 32 for b in corrupted)
print(flag.decode())