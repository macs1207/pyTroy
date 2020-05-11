from math import ceil

def prime():
    def is_prime(n):
        for i in range(5, current, 2):
            if current % i == 0:
                return False
        return True
    
    yield 2
    yield 3
        
    current = 5
    gap = 2
    while True:
        if is_prime(current):
            yield current
        
        current += gap
        gap = 6 - gap


n = eval(input("How many prime numbers do you want to get? "))
p = prime()
for i in range(n):
    print(next(p))
