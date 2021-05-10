from sample_files.other import qux


def foo():
    x = 1
    return bar(x)


def bar(a):
    return a + baz()


def baz():
    return 5 + qux()
