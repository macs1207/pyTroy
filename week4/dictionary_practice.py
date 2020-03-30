fruit_dict = {}

while True:
    row = input("輸入水果和數量，格式 {水果} {數量}:\n")
    if len(row.split(" ")) != 2:
        print("輸入格式錯誤\n---")
        continue
    
    fruit, quantity = row.split(" ")
    if fruit not in fruit_dict.keys():
        fruit_dict[fruit] = 0
    try:
        fruit_dict[fruit] += int(quantity)
    except ValueError as e:
        print("輸入格式錯誤\n---")
        continue
    
    print("---\n目前總計:")
    for key in fruit_dict.keys():
        print(f"{key} {fruit_dict[key]}")
    print("---")
