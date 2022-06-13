from numbers import Number


def formIfNum01(v) -> str:
    """
    圣遗物数字格式
    :param v: 数字
    :return:
    """
    if isinstance(v, (int, float)):
        if v == int(v):
            return f'%d' % v
        if abs(v) > 10:
            return f'%.0f' % v
        return f'%.1f%%' % (100 * v)
    return str(v)


def formIfNumhalfk(v) -> str:
    """
    程序数字格式，整数为整数，小于5为小数点后两位的百分数，小于500为小数点后两位，否则为小数点后一位
    :param v:
    :return:
    """
    if isinstance(v, Number):
        if v == int(v):
            return f'%d' % v
        if abs(v) < 5:
            return f'%.2f%%' % (100 * v)
        if abs(v) < 500:
            return f'%.2f' % v
        return f'%.1f' % v
    return str(v)


def stdform(x: dict) -> str:
    """
    用/分隔的圣遗物副词条格式
    :param x:
    :return:
    """
    return ' / '.join([f"{k}: {formIfNumhalfk(v)}" for k, v in x.items()])
