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
ENTER = ['\000', '\xe0']


def get_user_input(write_list):
    print ('A')
    user_input = EMPTY
    while write_list is not None and kbhit():
        keyboard = getch()
        if keyboard not in ENTER:
            user_input = user_input + keyboard
    if user_input is not EMPTY:
        return user_input

    return EMPTY


def main():
    client_socket = socket.socket()
    client_socket.connect((SERVER, PORT))
    print ('A')
    while True:
        read_list, write_list, error_list = select.select([client_socket], [client_socket], [])
        print ('B')
        print read_list
        print write_list
        if read_list is not None:
            print(client_socket.recv(KB))
        else:
            user_input = get_user_input(write_list)
            if user_input is not EMPTY:
                client_socket.send(user_input)

if __name__ == '__main__':
    main()