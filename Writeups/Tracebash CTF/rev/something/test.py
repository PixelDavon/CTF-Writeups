enc_bytes = [
    0xca, 0x89, 0xdb, 0x99, 0x8d, 0x86, 0xd8, 0x86,
    0xb4, 0x99, 0xdb, 0x93, 0xb4, 0x9d, 0xd8, 0x99
]

key_array = [0x54 ,   0x42 ,   0x43  ,  0x54  ,  0x46   , 0x7b] 

sixbytes = 0
for k in key_array:
    sixbytes ^= k

# Apply the math: Expected ^ sixbytes ^ 0xd7
d7_xor = 0xd7
decrypted_bytes = [b ^ sixbytes ^ d7_xor for b in enc_bytes]

# Reverse the string
flag_inner = "".join(chr(b) for b in reversed(decrypted_bytes))

print(f"TBCTF{{{flag_inner}}}")