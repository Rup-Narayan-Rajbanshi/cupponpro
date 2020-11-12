import random
import secrets


def gen_6digit_num():
    return str(random.randint(100002, 999997))


def make_hash_value():
    return secrets.token_hex(3)


def make_rand_username():
    return secrets.token_hex(5)
