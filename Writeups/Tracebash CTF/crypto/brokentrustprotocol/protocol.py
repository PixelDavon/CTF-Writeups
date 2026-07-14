from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import sha256
from random import randint
import os

p = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031

g = 2

a = randint(2,p-2)
b = randint(2,p-2)

A = pow(g,a,p)

# malicious client sends small subgroup element

B = p-1

shared = pow(B,a,p)

key = sha256(str(shared).encode()).digest()[:16]

iv = os.urandom(16)

flag = open("flag.txt","rb").read()

cipher = AES.new(key,AES.MODE_CBC,iv)

ct = cipher.encrypt(pad(flag,16))  #decrypt, unpad

print("p =",p)
print("g =",g)
print("A =",A)
print("B =",B)
print("iv =",iv.hex()) #unhex
print("ciphertext =",ct.hex()) #unhex
