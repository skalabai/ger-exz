import random
import hashlib


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def generate_prime(min_val, max_val):
    while True:
        num = random.randint(min_val, max_val)
        if is_prime(num):
            return num


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    d, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return d, x, y


def mod_inverse(e, phi):
    d, x, y = extended_gcd(e, phi)
    if d != 1:
        return -1
    return x % phi


def generate_keys():
    p = generate_prime(100, 500)
    q = generate_prime(100, 500)
    while q == p:
        q = generate_prime(100, 500)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 3
    while gcd(e, phi) != 1:
        e += 1

    d = mod_inverse(e, phi)

    return (e, n), (d, n)


def hash_message(text):
    h = hashlib.sha256(text.encode('utf-8')).hexdigest()
    return int(h, 16)


def sign_message(text, private_key):
    d, n = private_key
    h = hash_message(text) % n
    signature = pow(h, d, n)
    return signature


def verify_signature(text, signature, public_key):
    e, n = public_key
    h = hash_message(text) % n
    decrypted_hash = pow(signature, e, n)
    return h == decrypted_hash


public_key, private_key = generate_keys()

a = 0

while a == 0:
    text = input()
    mode = input()

    if mode == "1":
        signature = sign_message(text, private_key)
        print(signature)
    elif mode == "2":
        signature = int(input())
        is_valid = verify_signature(text, signature, public_key)
        print(is_valid)
    a = int(input())