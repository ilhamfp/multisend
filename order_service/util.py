from random import choice
from string import ascii_letters


def generate_token(length = 30):
    result = ''
    for _ in range(length):
        result += choice(ascii_letters)

    return result