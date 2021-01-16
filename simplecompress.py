# o = original string
# s = shortest non-existent string
# r = longest repeated string
# c = o with r replaced by s
# ^ = reverse of indicated string
# i = iteration
# compressed = {s}{r}{c}{-c[0]}{^r}{-r[0]}{^s}{i}
import itertools
import math
import os
import bitstring
import bitarray

tabSize = ""
def indent():
    global tabSize
    tabSize = tabSize + "  "
def outdent():
    global tabSize
    tabSize = tabSize[:-2]

def compress(o, iter, permOriginal):
    print(tabSize + "**compressing")
    indent()
    s = findS(o)
    print(tabSize + 's = ' + s)
    r = 0
    r = findR(r, o, s)
    print(tabSize + 'r = ' + r)
    c = o

    if r != "":
        cBody = permOriginal.replace(r, s)
        dBit1 = "1" if r[0] == "0" else "0"
        dBit2 = "1" if cBody[0] == "0" else "0"
        readable = s + ' ' + r + ' ' + cBody + ' ' + dBit2 + ' ' + r[::-1] + ' ' + dBit1 + ' ' + s[::-1] + ' ' + str(iter)
        c = readable.replace(" ", "", -1)
        if len(c) < len(o):
            print(tabSize + "(" + str(len(c)) + " bits) c = " + c[:50] + "... (" + readable[:50] + "...)")
            c2 = compress(c, 1, permOriginal)
            if len(c2) < len(c):
                return c2
    else:
        print(tabSize + "no R, compression not valuable returning previous iteration")

    outdent()
    if iter == 0:
        print(tabSize + "final compressed " + c[:50] + "...\n")
    return c

def findS(val):
    for x in range(0, len(val)):
        combos = list(["".join(seq) for seq in itertools.product(["0", "1"], repeat=x)])
        for s in combos:
            if s not in val:
                return s


def findR(longest, o, s):
    def savingsForWord(i, word, s):
        return ((i - 2) * len(word)) - ((i + 2) * len(s)) - 3
    bestCt = 0
    best = ""
    bestSavings = 0

    q = int(math.floor(len(o) / 4))
    indent()
    for rLen in range(len(s), q, 1):
        print("checking " + str(rLen))
        start = 0
        step = start
        indent()
        while start + (2*rLen) < len(o):
            toMatch = o[start:start + rLen]
            step = start + rLen
            instanceCt = 1
            indent()
            while step + rLen <= len(o):
                match = o[step:step + rLen]
                if match == toMatch:
                    step = step + rLen
                    instanceCt = instanceCt + 1
                else:
                    step = step + 1
            outdent()
            if instanceCt > 2:
                savings = savingsForWord(instanceCt, toMatch, s)
                if (savings > 0 and savings > bestSavings):
                    best = toMatch
                    bestCt = instanceCt
                    bestSavings = savings
            start = start + 1
        outdent()
    outdent()
    return best


def decompress(c):
    print(tabSize + "**decompressing")
    indent()
    iter = c[-1:]
    print(tabSize + "iter = " + iter)
    compressed = c[0:-1]
    rev = compressed[::-1]
    print(tabSize + "cmp = " + compressed[:50] + "...")
    print(tabSize + "rev = " + rev[:50] + "...")
    compressed = compressed.replace(" ", "", -1)
    rev = rev.replace(" ", "", -1)

    s = os.path.commonprefix([compressed, rev])
    compressed = compressed[len(s):-(len(s) + 2)]
    rev = rev[(len(s) + 1):-len(s)]
    print(tabSize + "s = '" + s + "'")

    r = os.path.commonprefix([compressed, rev])
    compressed = compressed[len(r):-len(r)]
    rev = rev[(len(r) + 1):-len(r)]

    rev = rev.replace(" ", "", 1)
    print(tabSize + "r = '" + r + "'")
    print(tabSize + "c body = " + compressed[:50] + "...")

    decompressed = compressed
    decompressed = decompressed.replace(s, r, -1)

    print(tabSize + "d body = " + decompressed[:50] + "...")

    outdent()
    if iter == "0":
        print(tabSize + "final decompressed " + decompressed[:50] + "...\n")
        return decompressed
    else:
        return decompress(decompressed)

def writeFile(s, fileName):
    with open(fileName, 'wb') as fh:
        bitarray.bitarray(s).tofile(fh)

# sample case
# s = 100
# r = 11111111111
# o = 00010 11111111111 11111111111 11111111111 11111111111 11111111111
# o = "000101111111111111111111111111111111111111111111111111111111"

# real case
o = bitstring.ConstBitStream(filename = 'test.gif').read("bin")

# main
print(" (" + str(len(o)) + " bits) o = " + o[:50] + "...\n")

c = compress(o, 0, o)
writeFile(c, "compressed.scmp")
d = decompress(c)
writeFile(d, "decompressed.gif")

print("o = " + o[:50] + "...")
print("d = " + d[:50] + "...")
print(o == d)
