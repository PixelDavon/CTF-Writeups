import os
import random
import sys
import tkinter as tk
idk = 'aEbOaqadaCapauaxacbiaCaEaFaLaSbPaCbKbGbtaxbqbLajbIaqbtbvbobJbiafalbtasbobLaraTabauapbnbebibLbeaibdabaXafafaabuaiagbLbCbLacbuapaXbN'
def encrypt(data):
    _ = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}'
    data = data[::(-1)]
    data = list(data)
    _n = len(data)
    for _i in range(_n):
        _j = (_i * 5 + 3) % _n
        _tmp = data[_i]
        data[_i] = data[_j]
        data[_j] = _tmp
    data = ''.join(data)
    _k = bytes([115, 110, 97, 107, 101, 122, 122])
    _out = bytearray()
    for _i, _c in enumerate(data.encode()):
        _r = _k[_i % len(_k)]
        _v = _c ^ _r
        _out.append(_v)
    _final = []
    for _v in _out:
        _a = _v // len(_)
        _b = _v - _a * len(_)
        _final.append(_[_a])
        _final.append(_[_b])
    return ''.join(_final)
root = tk.Tk()
root.attributes('-fullscreen', True)
root.configure(bg='black')
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.pack(fill='both', expand=True)
for y in range(0, height, 120):
    for x in range(0, width, 300):
        canvas.create_text(x, y, text='🦖🦖🦖🦖🦖🦖🦖🦖🦖', fill='#222222', font=('Arial', 40, 'bold'), anchor='nw')
def get_random_color():
    return f'#{random.randint(48, 255):02x}{random.randint(48, 255):02x}{random.randint(48, 255):02x}'
balls = []
for char in idk:
    size = random.randint(100, 140)
    x = random.randint(0, max(1, width - size))
    y = random.randint(0, max(1, height - size))
    color = get_random_color()
    rect_obj = canvas.create_rectangle(x, y, x + size, y + size, fill=color, outline='')
    font_size = int(size * 0.4)
    text_obj = canvas.create_text(x + size // 2, y + size // 2, text=char, fill='white', font=('Arial', font_size, 'bold'))
    dx = random.choice([(-1), 1]) * random.randint(3, 12)
    dy = random.choice([(-1), 1]) * random.randint(3, 12)
    balls.append({'rect': rect_obj, 'text': text_obj, 'x': x, 'y': y, 'dx': dx, 'dy': dy, 'size': size})
def animate():
    for ball in balls:
        ball['x'] += ball['dx']
        ball['y'] += ball['dy']
        size = ball['size']
        bounced = False
        if ball['x'] <= 0 or ball['x'] + size >= width:
            ball['dx'] *= (-1)
            ball['x'] = max(0, min(ball['x'], width - size))
            bounced = True
        if ball['y'] <= 0 or ball['y'] + size >= height:
            ball['dy'] *= (-1)
            ball['y'] = max(0, min(ball['y'], height - size))
            bounced = True
        if bounced:
            new_color = get_random_color()
            canvas.itemconfig(ball['rect'], fill=new_color)
        canvas.coords(ball['rect'], ball['x'], ball['y'], ball['x'] + size, ball['y'] + size)
        canvas.coords(ball['text'], ball['x'] + size // 2, ball['y'] + size // 2)
    root.after(16, animate)
def cleanup_and_exit(event=None):
    root.destroy()
    sys.exit(0)
initial_mouse_pos = None
root.bind('<Key>', cleanup_and_exit)
root.bind('<Button-1>', cleanup_and_exit)
root.bind('<Button-2>', cleanup_and_exit)
root.bind('<Button-3>', cleanup_and_exit)
animate()
root.mainloop()