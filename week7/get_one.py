cnt = 0

for i in range(1, 200):
    cnt += str(i).count("1")
    
print(cnt)