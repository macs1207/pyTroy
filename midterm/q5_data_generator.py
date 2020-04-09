import random

fruit = [
    "apple", "banana", "coconut", "zinfandel", "jujube", "durian", "grape", 
    "grapefruit", "guava", "lemon", "lichee", "orange", "kiwi", "mangosteen", 
    "mulberry", "papaya", "pear", "pineapple",
]

random.shuffle(fruit)

data = {}

for i in fruit:
    data[i] = 0

with open("q5_data.txt", "w") as f:
    for j in range(500):
        for i in fruit:
            increase = random.randint(1, 100)
            data[i] += increase
            f.writelines(f"{i} {increase}\n")
        
for i in data:
    print(f"{i} {data[i]}")
# print(f"{fruit} {random.randint(10)}")
