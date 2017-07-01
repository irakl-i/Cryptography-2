from oracle import *
import sys
import itertools


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def remove_padding(block):
    val = block[-1]
    res = block[:-val]
    padding = block[-val:]
    return res


def cleanup(result):
    result[-1] = remove_padding(result[-1])
    return convert(list(itertools.chain.from_iterable(result)))


def convert(bytes):
    return "".join(map(chr, bytes))


def get_response(p, n):
    return Oracle_Send(p, n) == 1


def decrypt(prev, cur, size):
    s = []
    for x in xrange(size):
        s.append(-sys.maxint + 1)

    for i in reversed(range(size)):
        prev_b = prev[:]

        for j in xrange(i + 1, size):
            prev_b[j] = prev[j] ^ s[j] ^ (size - i)

        pad = -1
        for k in xrange(0, 255):
            prev_b[i] = k
            if get_response(prev_b + cur, 2):
                if i == size - 1:
                    temp = prev_b[size - 2]
                    prev_b[size - 2] += 1
                    prev_b[size - 2] %= 256
                    if get_response(prev_b + cur, 2):
                        pad = k
                        prev_b[size - 2] = temp
                        break
                    prev_b[size - 2] = temp
                else:
                    pad = k
                    break

        s[i] = (size - i) ^ pad ^ prev[i]
        print s
    return s



#############################################
if len(sys.argv) < 2:
    print "Usage: python sample.py <filename>"
    sys.exit(-1)

f = open(sys.argv[1])
data = f.read()
f.close()

ctext = [(int(data[i:i + 2], 16)) for i in range(0, len(data), 2)]

# split ctext into chunks
clist = list(chunks(ctext, 16))
print clist
#############################################

Oracle_Connect()

result = list()
for first, second in itertools.izip(clist, clist[1:]):
    result.append(decrypt(first, second, 16))


result = cleanup(result)
print result


Oracle_Disconnect()
