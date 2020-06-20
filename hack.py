import socket
import sys

if len(sys.argv) == 4:
    IP = sys.argv[1]
    port = int(sys.argv[2])
    message = sys.argv[3]

    with socket.socket() as my_socket:
        address = (IP, port)
        my_socket.connect(address)

        data = message.encode()
        my_socket.send(data)
        response = my_socket.recv(1024)
        print(response.decode())
