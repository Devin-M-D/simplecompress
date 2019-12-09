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


def compress(o, iter):
    s = findS(o)
    print('s = ' + s)
    r = 0
    r = findR(r, o, s)
    print('r = ' + r)

    if r != "":
        cBody = o.replace(r, s)
        tComp = s + ' ' + r + ' ' + cBody + ' 1 ' + \
            r[::-1] + ' 1 ' + s[::-1] + ' ' + str(iter)
        print(o)
        print(tComp)
        print('len(o):' + str(len(o)))
        print('len(c):' + str(len(tComp)))
        if (2*len(s) + 2*len(r) + len(cBody) + 3) < len(o):
            dBit1 = "1" if r[0] == "0" else "0"
            dBit2 = "1" if cBody[0] == "0" else "0"
            c = s + ' ' + r + ' ' + cBody + ' ' + dBit2 + ' ' + \
                r[::-1] + ' ' + dBit1 + ' ' + s[::-1] + ' ' + str(iter)
            print('c = ' + c)
            #c = c.replace(" ", "", -1)
            c2 = compress(c, 1)
            if len(c2) < len(c):
                return c2
            return c
    return o


def findS(val):
    for x in range(0, len(val)):
        combos = set(["".join(seq)
                      for seq in itertools.product("01", repeat=x)])
        for s in combos:
            if s not in val:
                return s


def findR(longest, o, s):
    def savingsForWord(i, word, s):
        return (i * len(word)) - (i * len(s)) - 3
    ilongest = 0
    longest = ""
    h = math.floor(len(o) / 2)
    for x in range(h, 1, -1):
        start = 0
        while start + (2*x) <= len(o):
            curr = o[start:start + x]
            step = x
            i = 0
            while step + x <= len(o):
                match = o[step:step + x]
                if match == curr:
                    step = step + x
                    i = i + 1
                else:
                    step = step + 1
            if (savingsForWord(i, curr, s) > 0 and savingsForWord(i, curr, s) > savingsForWord(ilongest, longest, s)):
                longest = curr
                ilongest = i
            start = start+1
    return longest


def decompress(c):
    iter = c[-1:]
    print("iter = " + iter)
    c = c[0:-2]
    rev = c[::-1]
    print("com = " + c)
    print("rev = " + rev)
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
    print("com = " + c)
    print("rev = " + rev)
    c = c.replace(s, r, -1)

    c = c.replace(s, r, -1)
    print("com = " + c)
    print("rev = " + rev)

    if iter == "0":
        print("last decompress")
        return c
    else:
        return decompress(c)


# s = 100
# r = 11111111111
# 00010 11111111111 11111011111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111
# o = "101100010110001"
o = "000101111111111111111111111111111111111111111111111111111111"
print("o = " + o)
print("**compressing")
c = compress(o, 0)
#print("**decompressing ")
#d = decompress(c)
# print("**complete")
#print("new: " + d)
#print("ori: " + d)
