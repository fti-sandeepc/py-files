
a = [1,44,5,6,67,7,74,4,5,63,89,68]
m = 4
max_i = -10000
arr = []
for i in range(m):
    for i in a:
        if i>max_i:
            max_i=i
    a.remove(max_i)
    arr.append(max_i)
    max_i = -10000
print(arr)