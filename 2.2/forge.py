from oracle import *
import sys


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


if len(sys.argv) < 2:
    print "Usage: python sample.py <filename>"
    sys.exit(-1)

f = open(sys.argv[1])
data = f.read()
f.close()

Oracle_Connect()

dlist = list(chunks(data, 16))
tag = Mac(dlist[0] + dlist[1], len(dlist[0]) + len(dlist[1]))

for i in range(2, len(dlist), 2):
    b1 = bytearray(dlist[i])
    b = bytearray(len(b1))
    for x in range(len(b1)):
        b[x] = b1[x] ^ tag[x]
    tag = Mac(b + dlist[i + 1], 32)


ret = Vrfy(data, len(data), tag)

if ret == 1:
    print "Message verified successfully!"
else:
    print "Message verification failed."

Oracle_Disconnect()
