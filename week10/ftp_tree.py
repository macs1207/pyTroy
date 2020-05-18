from ftplib import FTP
from ftplib import error_perm

FTP_HOST = "ftp.ncnu.edu.tw"
FTP_PATH = "/FreeBSD"
FTP_USER = "ftp"

def scan_ftp_dir(ftp, path="/", show_file=True, depth=0, prefix=[], parent_is_last=True):

    def is_dir(ftp, path):
        try:
            ftp.cwd(path)
            return True
        except error_perm:
            return False

    def print_tree(path_name, depth, prefix):
        print(f'{"".join(prefix)}{"|   " if depth != 0 else ""}')
        if path_name == "/":
            path_name = ftp.host
        print(f'{"".join(prefix)}{"+---" if depth != 0 else ""}{path_name}')
        
    if is_dir(ftp, path):            
        dir_list = sorted(ftp.nlst())
        print_tree(path, depth, prefix)

        for name in dir_list:                                    
            if depth > 0:
                if parent_is_last:
                    prefix.append("    ")
                else:
                    prefix.append("|   ")
            is_last = dir_list.index(name) == (len(dir_list) - 1)
            prefix = scan_ftp_dir(ftp, name, show_file, depth + 1, prefix, is_last)
        ftp.cwd("..")
    elif show_file:
        print_tree(path, depth, prefix)
    
    if len(prefix) > 0:
        prefix.pop(-1)
    return prefix

def main():
    ftp = FTP(FTP_HOST)
    ftp.login(FTP_USER)
    
    print("Show with file:", end='')
    scan_ftp_dir(ftp, FTP_PATH)
    print()
    
    print("Show without file:", end='')
    scan_ftp_dir(ftp, FTP_PATH, show_file=False)
    
    ftp.quit()
    
main()