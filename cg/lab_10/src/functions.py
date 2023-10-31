import math as m


def f0(x, z):
    return m.cos(x) * m.sin(z)


def f1(x, z):
    return m.sqrt(m.fabs(x * z))


def f2(x, z):
    return m.exp(m.cos(x) * m.sin(z))


def f3(x, z):
    return m.sin(x * z)
