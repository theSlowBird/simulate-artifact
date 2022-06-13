from collections import Counter


add = [
    (0.7, 0, 0, 0),
    (0, 0.7, 0, 0),
    (0, 0, 0.7, 0),
    (0, 0, 0, 0.7),
    (0.8, 0, 0, 0),
    (0, 0.8, 0, 0),
    (0, 0, 0.8, 0),
    (0, 0, 0, 0.8),
    (0.9, 0, 0, 0),
    (0, 0.9, 0, 0),
    (0, 0, 0.9, 0),
    (0, 0, 0, 0.9),
    (1, 0, 0, 0),
    (0, 1, 0, 0),
    (0, 0, 1, 0),
    (0, 0, 0, 1),
]


def enhance(k):
    if k == 0:
        return [(0, 0, 0, 0)]
    ret = []
    for x in enhance(k-1):
        for y in add:
            ret.append(tuple(x[i]+y[i] for i in range(4)))
    return ret

x = []
for i in range(6):
    x.append(dict(Counter(enhance(i))))

with open('pre.txt', 'w') as fout:
    fout.write(str(x))