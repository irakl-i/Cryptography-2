from oracle import *
import sys
import itertools


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def remove_padding(block):
    val = block[-1]
    res = block[:-val]
    return res


def cleanup(result):
    result[-1] = remove_padding(result[-1])
    return convert(list(itertools.chain.from_iterable(result)))


def convert(bytes):
    return "".join(map(chr, bytes))


def get_response(p, n):
    return Oracle_Send(p, n) == 1


def get_pad(block, cur, index, size):
    pad = -sys.maxint + 1
    for i in xrange(0, 255):
        block[index] = i
        if get_response(block + cur, 2):
            if index == size - 1:
                temp = block[size - 2]
                block[size - 2] += 1
                block[size - 2] %= 256
                if get_response(block + cur, 2):
                    pad = i
                    block[size - 2] = temp
                    return pad
                block[size - 2] = temp
            else:
                pad = i
                return pad
    return pad


def decrypt(prev, cur, size):
    s = []
    for x in xrange(size):
        s.append(-sys.maxint + 1)

    for i in reversed(range(size)):
        prev_b = list(prev)

        for j in xrange(i + 1, size):
            prev_b[j] = prev[j] ^ s[j] ^ (size - i)

        pad = get_pad(prev_b, cur, i, size)

        s[i] = prev[i] ^ (size - i) ^ pad
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
