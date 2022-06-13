from typing import Iterable

import numpy as np


def midNums(lis: Iterable, len):
    print(f'{lis[(len-1)//2:len//2+1] = }')
    return np.average(lis[(len - 1) // 2:len // 2 + 1], 0)


lis = np.array([
    [1, 2],
    [3, 4],
    [5, 9],
    [7, 8],
])
print(lis, lis.shape)
print(midNums(lis, lis.shape[0]))
print()
lis = np.concatenate((lis, np.empty((0, 2)), [[1, 3]]))
print(lis)

print(midNums(lis, lis.shape[0]))

print(f'{1/lis = }')

print(type(lis))

x = np.array([1, 3])
x
y = np.array([x, list(map(lambda k:k ** 2, x))])
y
np.array(np.nditer(y, order='F'))