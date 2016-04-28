import socket
import select
from ChatClasses import *
from time import gmtime, strftime

__author__ = 'Gilad Barak'

PORT = 23
SELF_ASSIGN_SERVER = '0.0.0.0'
NUMBER_OF_LISTENING = 5
KB = 1024
EMPTY = ''
EMPTY_DATA = ['']
UNKNOWN_USERNAME = 'Unknown'
CONNECTION_CLOSED = 'Someone closed connection'
MESSAGE_TEMPLATE = '{} {}: {}'
IS_ADMIN_DEFAULT = False
IS_MUTED_DEFAULT = False
QUITING_MESSAGE = 'quit'
MESSAGE_SEPARATOR = '|'
USERNAME_LENGTH_INDEX = 0
USERNAME_INDEX = 1
FUNCTION_INDEX = 2
MESSAGE_LENGTH_INDEX = 3
MESSAGE_INDEX = 4
MESSAGE_PROTOCOL_CODE = '1'
TIME_FORMAT = "%H:%M"
MESSAGE_PROTOCOL_FORMAT = '{}|{}'
LEFT_CHAT_MESSAGE = 'has left the chat!'


def parse_message(message):
    """
    :param message: got from client socket
    :return : parsed into list [length of user name, user name, length of message, message]
    """
    return message.split(MESSAGE_SEPARATOR)


def close_connection(chat_users, current_socket):
    """
    :param chat_users: dictionary that contains {Socket:User}
    :param current_socket: one of connected client's socket
    """
    left_chat_notification = MESSAGE_TEMPLATE.format(strftime(TIME_FORMAT),
                                                     chat_users[current_socket].user_name, LEFT_CHAT_MESSAGE)

    left_chat_notification = MESSAGE_PROTOCOL_FORMAT.format(len(left_chat_notification), left_chat_notification)

    for user in chat_users.keys():
        user.send(left_chat_notification)

    print(left_chat_notification)

    chat_users.pop(current_socket)
    current_socket.close()


def manage_data(current_socket, chat_users, messages_to_send):
    """
    :param current_socket: one of connected client's socket
    :param chat_users: dictionary that contains {Socket:User}
    :param messages_to_send: List of tuples (sender socket, message)
    """
    data = parse_message(current_socket.recv(KB))

    if data == EMPTY_DATA:
        close_connection(chat_users, current_socket)
        return

    elif data[FUNCTION_INDEX] == MESSAGE_PROTOCOL_CODE:
        if data[MESSAGE_INDEX] == QUITING_MESSAGE:
                close_connection(chat_users, current_socket)
                return

        elif data[MESSAGE_INDEX] != EMPTY and chat_users[current_socket] == UNKNOWN_USERNAME:
            chat_users[current_socket] = ChatUser(data[USERNAME_INDEX], IS_ADMIN_DEFAULT, IS_MUTED_DEFAULT)

        else:
            messages_to_send.append((current_socket, data[MESSAGE_INDEX]))


def manage_chat(server_socket, chat_users, messages_to_send):
    """
    :param server_socket: socket server sends through
    :param chat_users: dictionary that contains {Socket:User}
    :param messages_to_send: List of tuples (sender socket, message)
    manages chat as server
    """
    read_list, write_list, error_list = select.select([server_socket] + chat_users.keys(),
                                                      chat_users.keys(), [])
    for current_socket in read_list:
        if current_socket is server_socket:
            (new_socket, address) = current_socket.accept()
            chat_users[new_socket] = UNKNOWN_USERNAME
        else:
            manage_data(current_socket, chat_users, messages_to_send)

    send_waiting_messages(write_list, messages_to_send, chat_users)


def init_server():
    """
    Initiates server settings and sockets.
    """
    server_socket = socket.socket()
    server_socket.bind((SELF_ASSIGN_SERVER, PORT))
    server_socket.listen(NUMBER_OF_LISTENING)
    return server_socket


def send_waiting_messages(write_list, messages_to_send, chat_users):
    """
    :param write_list: Sockets available to write to
    :param messages_to_send: List of tuples (sender socket, message)
    Sends data to all chat users except the sender and clears list
    """
    for message in messages_to_send:
        (client_socket, data) = message
        for user in write_list:
            if user is not client_socket:
                proto = MESSAGE_TEMPLATE.format(strftime(TIME_FORMAT), chat_users[client_socket].user_name, data)
                user.send(MESSAGE_PROTOCOL_FORMAT.format(len(proto), proto))
        a = MESSAGE_TEMPLATE.format(strftime(TIME_FORMAT), chat_users[client_socket].user_name, data)
        print(MESSAGE_PROTOCOL_FORMAT.format(str(len(a)), a))
        messages_to_send.remove(message)


def main():
    server_socket = init_server()
    chat_users = {}
    messages_to_send = []
    while True:
        manage_chat(server_socket, chat_users, messages_to_send)

if __name__ == '__main__':
    main()