with open("ciphertext.bin", "rb") as f:
    ciphertext = f.read()

# for x,y in zip(ciphertext,'TBCTF{'):
#     print(x^ord(y),end=' ')

# Output: 184 238 11 75 147 186 
# low bytes of hex of freq

Aminor = [440, 494, 523, 587, 659, 698, 784, 880]
low = [h&0xff for h in Aminor]
print(low)

for i in range(len(ciphertext)):
    print(chr(ciphertext[i]^low[i%len(low)]),end='')