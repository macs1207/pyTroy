import os

PATH = "Ch07"

def scan_dir(path):
    result = []
    if os.path.isdir(path):
        for name in os.listdir(path):
            fullpath = os.path.join(path, name)
            result += scan_dir(fullpath)
    else:
        result.append(path)
    return result


for fn in scan_dir(PATH):
    print(fn, os.path.getsize(fn))
