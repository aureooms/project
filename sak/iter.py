import lib.args
import lib.sys
import fileinput
import itertools
import getpass
import lib.file
import lib.iterator

# polyfill for generator zip function

if hasattr(itertools, "izip"):
    _zip = itertools.izip

else:
    _zip = zip


def directories(callable=None, iterable=None):

    iterable = lib.args.listify(iterable)
    callable = lib.args.listify(callable)

    callable = list(itertools.chain(*map(lib.args.split, callable)))

    iterable = lib.iterator.input(iterable)

    for item in iterable:

        lib.sys.call(callable, stddefault=None, cwd=item)


def imap(callable=None, iterable=None):

    iterable = lib.args.listify(iterable)
    callable = lib.args.listify(callable)

    callable = list(itertools.chain(*map(lib.args.split, callable)))

    iterable = lib.iterator.input(iterable)

    for item in iterable:

        lib.sys.call([arg.format(item) for arg in callable], stddefault=None)


def starmap(callable=None, iterable=None):

    iterable = lib.args.listify(iterable)
    callable = lib.args.listify(callable)

    callable = list(itertools.chain(*map(lib.args.split, callable)))

    iterable = lib.iterator.input(iterable)

    for item in iterable:

        argv = lib.args.split(item)

        args, kwargs = lib.args.parse(argv, [], {})

        lib.sys.call([arg.format(*args, **kwargs)
                      for arg in callable], stddefault=None)


@lib.args.convert(n=int)
def repeat(iterable=None, n=-1):
    """
            Repeat given lines n times. If n is negative then repeat given string an infinite number of times.
    """

    iterable = lib.args.listify(iterable)

    iterable = lib.iterator.input(iterable)

    args = [None] if n < 0 else [None, n]

    for _ in itertools.repeat(*args):
        for item in iterable:
            print(item)


@lib.args.convert(n=int)
def password(n=-1):

    item = getpass.getpass('Password to repeat : ')
    repeat(item, n)


def izip(callables=None, sep=" "):

    callables = lib.args.listify(callables)

    callables = map(lib.args.split, callables)

    iterables = [lib.file.lineiterator(lib.sys.popen(
        callable).stdout) for callable in callables]

    for t in _zip(*iterables):

        print(*t, sep=sep)


@lib.args.convert(start=int)
def count(start=0):

    while True:

        print(start)

        start += 1


@lib.args.convert(start=int, stop=int)
def range(start, stop):

    while start < stop:

        print(start)

        start += 1
