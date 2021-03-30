from incompatible_library import math_funcs


def add_some_numbers(a: int, b: int):
    return math_funcs.add(a, b)


def subtract_some_numbers(a: int, b: int):
    return math_funcs.sub(a, b)


def multiply_some_numbers(a: int, b: int):
    return math_funcs.mult(a, b)


def divide_some_numbers(a: int, b: int):
    return math_funcs.div(a, b)


def floor_divide_some_numbers(a: int, b: int):
    return math_funcs.floordiv(a, b)
