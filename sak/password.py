
from os import urandom
from random import seed, choice
import lib.args


@lib.args.convert(n=int)
def new(n, forbidden=''):

    seed(urandom(n))

    allowed = "azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN`!$%^&*()_+-=;,./<>?1234567890'\"§èçé#@|{}àùµ"

    symbols = list(frozenset(allowed) - frozenset(forbidden))

    print("".join([choice(symbols) for i in range(n)]))


@lib.args.convert(n=int)
def bytes(n):

    print(" ".join(map(lambda x: hex(int(x))[2:], urandom(n))))


def hexadecimal(password):

    print(" ".join(list(map(lambda x: hex(ord(x))[2:], password))))


def ascii(*bytes):

    print("".join(list(map(lambda x: chr(int(x, 16)), bytes))))
