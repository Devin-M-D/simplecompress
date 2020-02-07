# o = original string
# s = shortest non-existent string
# r = longest repeated string
# c = o with r replaced by s
# ^ = reverse of indicated string
# i = iteration
# src{-c[0]}{^r}{-r[0]}{^s}{i}
import itertools
import math
import os


def compress(o, iter, permOriginal):
    s = findS(o)
    print('s = ' + s)
    r = 0
    r = findR(r, o, s)
    print('r = ' + r)
    c = o

    if r != "":
        cBody = permOriginal.replace(r, s)
        dBit1 = "1" if r[0] == "0" else "0"
        dBit2 = "1" if cBody[0] == "0" else "0"
        readable = s + ' ' + r + ' ' + cBody + ' ' + dBit2 + ' ' + r[::-1] + ' ' + dBit1 + ' ' + s[::-1] + ' ' + str(iter)
        c = readable.replace(" ", "", -1)
        print("permOriginal = ", permOriginal)
        print("readable = ", readable)
        print("c = ", c)
        print('len(permOriginal):' + str(len(permOriginal)))
        print('len(c):' + str(len(c)))
        c2 = compress(c, iter + 1, permOriginal)
        if len(c2) < len(c):
            return c2
        return c
    else:
        print("no R, compression not valuable returning previous iteration")
    return c


def findS(val):
    for x in range(0, len(val)):
        combos = set(["".join(seq)
                      for seq in itertools.product("01", repeat=x)])
        for s in combos:
            if s not in val:
                return s


def findR(longest, o, s):
    def savingsForWord(i, word, s):
        return ((i - 2) * len(word)) - ((i + 2) * len(s)) - 3
    bestCt = 0
    best = ""
    bestSavings = 0
    h = int(math.floor(len(o) / 2))
    for rLen in range(h, 1, -1):
        start = 0
        while start + (2*rLen) <= len(o):
            toMatch = o[start:start + rLen]
            #print("toMatch = ", toMatch)
            step = rLen
            instanceCt = 0
            while step + rLen <= len(o):
                match = o[step:step + rLen]
                if match == toMatch:
                    step = step + rLen
                    instanceCt = instanceCt + 1
                else:
                    step = step + 1
            savings = savingsForWord(instanceCt, toMatch, s)
            if (savings > 0 and savings > bestSavings):
                best = toMatch
                bestCt = instanceCt
                bestSavings = savingsForWord(bestCt, best, s)
                print("new best r! r is", best, "savings is ", bestSavings)
            start = start+1
    return best


def decompress(c):
    iter = c[-1:]
    print("iter = " + iter)
    c = c[0:-1]
    rev = c[::-1]
    print("c = " + c)
    print("reversed = " + rev)
    c = c.replace(" ", "", -1)
    rev = rev.replace(" ", "", -1)

    s = os.path.commonprefix([c, rev])
    c = c[len(s):-(len(s) + 2)]
    rev = rev[(len(s) + 1):-len(s)]
    #c = c[:-1]
    print("s = '" + s + "'")
    #print("com = " + c)
    #print("rev = " + rev)

    r = os.path.commonprefix([c, rev])
    c = c[len(r):-(len(r) + 2)]
    rev = rev[(len(r) + 1):-len(r)]

    rev = rev.replace(" ", "", 1)
    print("r = '" + r + "'")
    print("c = " + c)
    print("reversed = " + rev)
    c = c.replace(s, r, -1)

    c = c.replace(s, r, -1)
    print("c = " + c)
    print("reversed = " + rev)

    if iter == "0":
        print("last decompress")
        return c
    else:
        return decompress(c)


# s = 100
# r = 11111111111
# 00010 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111
       #1111111111
# o = "101100010110001"
o = "000101111111111111111111111111111111111111111111111111111111"
print("o = " + o)
print("**compressing")
c = compress(o, 0, o)
print(c)
print("**decompressing")
d = decompress(c)
print("o", o)
print("d", d)
print(o==d)
#print("**decompressing ")
#d = decompress(c)
# print("**complete")
#print("new: " + d)
#print("ori: " + d)
