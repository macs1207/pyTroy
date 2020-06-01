fn = input("Filename? ")
try:
    infile = open(fn, "r")
    s = infile.read()
    print(s)
    infile.close()
except FileNotFoundError as e:
    # 找不到檔案引發例外
    print(f'{e.args[0]}: {e.args[1]}')
except PermissionError as e:
    # 沒有讀寫檔案權限引發例外
    print(f'{e.args[0]}: {e.args[1]}')
except Exception as e:
    print(f'{e.args[0]}: {e.args[1]}')
    
print("Program ends gracefully.")
