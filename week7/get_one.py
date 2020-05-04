def solution1(n):
    cnt = 0

    for i in range(1, n + 1):
        cnt += str(i).count("1")
    print(cnt)

def solution2(n):
    print(sum([str(i).count('1') for i in range(n + 1)]))

n = 199
solution1(n)
solution2(n)