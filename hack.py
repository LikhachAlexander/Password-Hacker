import socket
import sys
import itertools
from string import ascii_lowercase, digits

max_length = 5
max_tries = 10000000

alphabet = ascii_lowercase + digits


def get_passwords():
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


if len(sys.argv) == 3:
    IP = sys.argv[1]
    port = int(sys.argv[2])

    with socket.socket() as my_socket:
        address = (IP, port)
        my_socket.connect(address)
        # create generator
        passwords = get_passwords()
        for _i in range(max_tries):
            try:
                password = next(passwords)
                data = password.encode()
                my_socket.send(data)
                response = my_socket.recv(1024).decode()
                if response == "Connection success!":
                    print(password)
                    break
            except StopIteration:
                break

else:
    passwords = get_passwords()
    for _i in range(max_tries):
        try:
            password = next(passwords)
            print(password)
        except StopIteration:
            break
