#
# 9618 built-in function stubs for generated Python preview only.
# Not executed by the checker in MVP.


def LENGTH(s):
    return len(s)


def LEFT(s, n):
    return s[:n]


def RIGHT(s, n):
    return s[-n:]


def MID(s, start, length):
    return s[start - 1 : start - 1 + length]


def LCASE(c):
    return c.lower()


def UCASE(c):
    return c.upper()


def TO_UPPER(s):
    return s.upper()


def TO_LOWER(s):
    return s.lower()


def NUM_TO_STR(n):
    return str(n)


def STR_TO_NUM(s):
    return int(s)


def IS_NUM(s):
    return s.isdigit()


def ASC(c):
    return ord(c)


def CHR(n):
    return chr(n)


def RAND(n):
    import random

    return random.randint(1, n)


def RANDOM():
    import random

    return random.random()


def ROUND(n, places=0):
    return round(n, places)


def MOD(a, b):
    return a % b


def DIV(a, b):
    return a // b


def EOF(filename):
    return False
