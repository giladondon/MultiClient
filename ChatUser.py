import socket
import select
from msvcrt import kbhit
from msvcrt import getch
from ChatClasses import *

__author__ = 'user'

KB = 1024
EMPTY = ''
PORT = 23
SERVER = '192.168.1.84'
ENTER = '\r'
SEND_FLAG_INDEX = 0
MESSAGE_INDEX = 1
CLIENT_SOCKET_INDEX = 0
USERNAME_MESSAGE = "Hello and welcome to our chat! please type your username: "
USERNAME_TEMPLATE = '{}\r'
SEMI_FULL = ' '
USER_NAME_INDEX = 1
CHAT_MESSAGE_CODE = 1
PROTOCOL_TEMPLATE = '{}|{}|{}|{}|{}'


def get_user_input(user_input):
    """
    :param user_input: What user inputted up till now.
    :return : True if message is to send now, final user message
    """
    if kbhit():
        keyboard = getch()
        if keyboard != ENTER:
            user_input = user_input + keyboard
            return False, user_input
        else:
            return True, user_input

    return False, user_input


def should_send(data, write_list, user_name):
    """
    :param data: is message ready to be sent, message
    :param write_list: Sockets available to write to
    :param user_name: user name given by user
    """
    if write_list and data[SEND_FLAG_INDEX]:
        write_list[CLIENT_SOCKET_INDEX].send(PROTOCOL_TEMPLATE.format(len(user_name), user_name, CHAT_MESSAGE_CODE,
                                                                      len(data[MESSAGE_INDEX]), data[MESSAGE_INDEX]))
        return EMPTY

    return data[MESSAGE_INDEX]


def set_setting():
    """
    Set all settings of chat user:
    User name, socket
    """
    user_name = raw_input(USERNAME_MESSAGE)
    client_socket = socket.socket()
    client_socket.connect((SERVER, PORT))
    user_input = USERNAME_TEMPLATE.format(user_name)
    should_send((True, user_input), [client_socket])

    return client_socket, user_name


def main():
    data = set_setting()
    client_socket = data[CLIENT_SOCKET_INDEX]
    user_name = data[USER_NAME_INDEX]
    user_input = EMPTY
    while data != EMPTY:
        read_list, write_list, error_list = select.select([client_socket], [client_socket], [])
        if read_list:
            data = client_socket.recv(KB)
            print(data)
        user_input = should_send(get_user_input(user_input), write_list, user_name)
    print ('Sorry but U are out!')


if __name__ == '__main__':
    main()