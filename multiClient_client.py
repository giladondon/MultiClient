import socket

__author__ = 'Gilad Barak'
__name__ = 'main'

PORT = 23
SERVER = '192.168.1.84'
KB = 1024
EMPTY = ''


def handle_user(client_socket):
    name = raw_input('Mr. Server is asking for your name...')
    client_socket.send(name)
    print(client_socket.recv(KB))


def main():
    client_socket = socket.socket()
    client_socket.connect((SERVER, PORT))
    while True:
        handle_user(client_socket)


if __name__ == 'main':
    main()