import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("path")
parser.add_argument("-f", "--file", action="store_true", help="show file in the tree")
args = parser.parse_args()

def scan_dir(path, show_file=True, depth=0, prefix=[], parent_is_last=True):

    def print_tree(path_name, depth, prefix):
        for i in prefix:
            print(i, end='')
        print(f'{"|   " if depth != 0 else ""}')
        
        for i in prefix:
            print(i, end='')
        print(f'{"+---" if depth != 0 else ""}{path_name}')
        
    if os.path.isdir(path):            
        dir_list = sorted(os.listdir(path))
        print_tree(os.path.split(path)[1], depth, prefix)

        for name in dir_list:
            fullpath = os.path.join(path, name)
                                    
            if depth > 0:
                if parent_is_last:
                    prefix.append("    ")
                else:
                    prefix.append("|   ")
            is_last = dir_list.index(name) == (len(dir_list) - 1)
            prefix = scan_dir(fullpath, show_file, depth + 1, prefix, is_last)
    elif show_file:
        print_tree(os.path.split(path)[1], depth, prefix)
    
    if len(prefix) > 0:
        prefix.pop(-1)
    return prefix


scan_dir(args.path, args.file)
