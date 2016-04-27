import socket
import select
from msvcrt import kbhit
from msvcrt import getch

__author__ = 'user'

KB = 1024
EMPTY = ''
PORT = 23
SERVER = '192.168.1.84'
SELF_ASSIGNED_IP = '0.0.0.0'
ENTER = '\r'
SEND_FLAG_INDEX = 0
MESSAGE_INDEX = 1


def get_user_input(user_input):
    if kbhit():
        keyboard = getch()
        if keyboard != ENTER:
            user_input = user_input + keyboard
            return False, user_input
        else:
            print('ENTER!')
            return True, user_input

    return False, user_input


def should_send(data, write_list, client_socket):
    if write_list and data[SEND_FLAG_INDEX]:
        client_socket.send(data[MESSAGE_INDEX])
        return EMPTY

    return data[MESSAGE_INDEX]


def main():
    client_socket = socket.socket()
    client_socket.connect((SERVER, PORT))
    user_input = EMPTY
    while True:
        read_list, write_list, error_list = select.select([client_socket], [client_socket], [])
        if read_list:
            print ('E')
            print(client_socket.recv(KB))
        user_input = should_send(get_user_input(user_input), write_list, client_socket)


if __name__ == '__main__':
    main()