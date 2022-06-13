from matplotlib import pyplot as plt
import numpy as np

data = np.array([
    40895.0,
    44197.9,
    45750.2,
    46800.4,
    47568.1,
    48171.5,
    48678.6,
    49117.0,
    49449.4,
    49740.8,
    50035.1,
    50262.8,
    35655.0,
    38283.6,
    39653.8,
    40518.0,
    41164.2,
    41654.3,
    42064.3,
    42429.1,
    42726.6,
    43001.0,
    43237.2,
    43455.4,
    34123.0,
    36581.2,
    37814.5,
    38576.5,
    39179.9,
    39624.6,
    39989.6,
    40320.8,
    40592.8,
    40811.3,
    41025.5,
    41211.4,
])

data_betterer = np.array([
    27.28,
    30.73,
    32.29,
    33.31,
    34.02,
    34.61,
    35.07,
    35.47,
    35.77,
    36.05,
    36.29,
    36.51,
    24.88,
    28.14,
    29.67,
    30.65,
    31.29,
    31.82,
    32.28,
    32.65,
    33.01,
    33.29,
    33.53,
    33.75,
    27.90,
    30.94,
    32.43,
    33.34,
    34.01,
    34.51,
    34.89,
    35.25,
    35.54,
    35.83,
    36.08,
    36.25,
])

data.shape = (3, 12)
data_betterer.shape = data.shape
label = [
    '护摩之杖',
    '匣里灭辰',
    '决斗枪',
]

print(data)
print(data.shape)

plt.rcParams['font.sans-serif'] = ['DengXian']
# plt.rcParams['font.sans-serif'] = ['SimSun']
# plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

for i in range(data.shape[0]):
    plt.plot(np.arange(12) + 1, data[i, ...], label=label[i])

plt.legend()
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1))
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(1000))
plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(.5))
plt.gca().yaxis.set_minor_locator(plt.MultipleLocator(500))
plt.xlabel('betterer_month')
plt.ylabel('目标函数：伤害期望')
CHARACTER = ['Hu Tao', 'Kamisato Ayaka', 'Yoimiya', 'Sayu'][0]
plt.savefig('%s.png' % CHARACTER, dpi=400)
# plt.show()
plt.clf()

for i in range(data_betterer.shape[0]):
    plt.plot(np.array(range(data_betterer.shape[1])) + 1, data_betterer[i, ...], label=label[i])

plt.legend()
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1))
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(1))
plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(.5))
plt.gca().yaxis.set_minor_locator(plt.MultipleLocator(.5))
plt.xlabel('betterer_month')
plt.ylabel('betterer词条/目标函数：伤害期望')
plt.savefig('%s_betterer.png' % CHARACTER, dpi=400)
# plt.show()
