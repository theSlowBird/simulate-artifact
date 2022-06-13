import numpy as np
import pyperclip

pyperclip.copy('''PERSONS = 4000 effect  Weight damage Weight  cure           Weight  increment
1 month(s)     5051.4  50.0   4245.3 71.8    6018.5         28.2           0
2 month(s)     5225.5  51.5   4510.0 74.5    6057.5         28.4           0
3 month(s)     5317.4  52.3   4662.1 76.0    6068.3         28.5           0
4 month(s)     5374.7  52.7   4759.7 77.0    6075.4         28.6           0
5 month(s)     5419.2  53.1   4838.7 77.7    6084.0         28.6           0
6 month(s)     5454.4  53.4   4896.3 78.2    6089.6         28.7           0
7 month(s)     5481.3  53.6   4943.3 78.6    6092.1         28.7           0
8 month(s)     5505.1  53.8   4983.8 79.0    6093.7         28.7           0
9 month(s)     5525.3  54.0   5022.6 79.4    6095.3         28.7           0
10 month(s)    5545.5  54.1   5053.6 79.6    6092.9         28.7           0
11 month(s)    5561.7  54.3   5083.1 79.9    6094.9         28.7           0
12 month(s)    5576.3  54.4   5111.1 80.1    6097.1         28.7           0
''')



def func1(x: list):
    # print(type(x), x)
    if x[0] == 'PERSONS':
        return [' '.join(x[0:3])] + x[3:]
    if x[1] == 'month(s)':
        return [' '.join(x[0:2])] + x[2:]


def main():
    if not hasattr(main, 'dout'):
        main.dout = ''
    if main.dout == pyperclip.paste():
        return
    paste = pyperclip.paste().replace('Damage2Weight', 'Weight').replace('Effect2Weight', 'Weight')
    data = np.array(paste.strip().splitlines())
    # print(data)
    data = np.char.strip(data)
    # print(data)
    print(f'{data.size = }, {data.shape = }')
    data = np.char.split(data)
    # print(data)
    print(f'{data.size = }, {data.shape = }')
    data = np.array(list(map(func1, data)))
    # print(data)
    print(f'{data.size = }, {data.shape = }')

    for j in np.arange(data.shape[1]):
        l = max([len(data[i, j]) for i in np.arange(data.shape[0])])
        print(l)
        for i in np.arange(data.shape[0]):
            data[i, j] = f'%-{l}s' % data[i, j]

    # print(data)

    main.dout = '\n'.join(['   '.join(x) for x in data])

    print(main.dout)
    pyperclip.copy(main.dout)


while True:
    main()
