from math import ceil

test_list = list(range(22))
print(test_list)

x = 5

print(ceil(6 / 10))

for a in range(ceil(len(test_list) / x)):
    print(test_list[a * ceil(len(test_list) / x):
                    (a + 1) * ceil(len(test_list) / (x))])

a = [1 for x in range(5)]
print(a)


print('Hello World!')
