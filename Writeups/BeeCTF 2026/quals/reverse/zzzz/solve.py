def decrypt(data):
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}'

    out = bytearray()
    for i in range(0, len(data), 2):
        a = chars.index(data[i])
        b = chars.index(data[i+1])
        out.append(a * len(chars) + b)

    key = b'snakezz'
    for i in range(len(out)):
        out[i] ^= key[i % len(key)]

    text = list(out.decode())
    n = len(text)
    for i in range(n-1, -1, -1):
        j = (i*5+3) % n
        text[i], text[j] = text[j], text[i]
    return ''.join(text)[::-1]

print(decrypt('aEbOaqadaCapauaxacbiaCaEaFaLaSbPaCbKbGbtaxbqbLajbIaqbtbvbobJbiafalbtasbobLaraTabauapbnbebibLbeaibdabaXafafaabuaiagbLbCbLacbuapaXbN'
))