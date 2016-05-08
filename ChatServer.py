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
KICK_OUT_CODE = '3'
TIME_FORMAT = "%H:%M"
MESSAGE_PROTOCOL_FORMAT = '{}|{}'
LEFT_CHAT_MESSAGE = 'has left the chat!'
KICKED_OUT_MESSAGE = 'has been kicked out from the chat!'
ADMINS = set(['Giladondon', 'Miki', 'Admin'])
ADMIN_AT = '@'
ADMIN_STATUS_NOTIFICATION = 'ADMIN'


def get_key_by_value(dict, search_value):
    """
    :param dict: dictionary
    :return key: key of value
    """
    for key, value in dict.iteritems():
        if value.user_name == search_value:
            return key
    return None


def ignite_user(user_name):
    """
    :param user_name: string representing user_name of user
    Sets every new user connected
    """
    user = ChatUser(user_name, IS_ADMIN_DEFAULT, IS_MUTED_DEFAULT)
    if user_name in ADMINS:
        user.is_admin = True
        user.user_name = ADMIN_AT + user.user_name
    return user


def parse_message(message):
    """
    :param message: got from client socket
    :return : parsed into list [length of user name, user name, length of message, message]
    """
    return message.split(MESSAGE_SEPARATOR)


def close_connection(chat_users, current_socket, is_kicked):
    """
    :param chat_users: dictionary that contains {Socket:User}
    :param current_socket: one of connected client's socket
    """
    if current_socket:
        if is_kicked:
            left_chat_notification = MESSAGE_TEMPLATE.format(strftime(TIME_FORMAT),
                                                             chat_users[current_socket].user_name, KICKED_OUT_MESSAGE)
        else:
            left_chat_notification = MESSAGE_TEMPLATE.format(strftime(TIME_FORMAT),
                                                             chat_users[current_socket].user_name, LEFT_CHAT_MESSAGE)

        left_chat_notification = MESSAGE_PROTOCOL_FORMAT.format(len(left_chat_notification), left_chat_notification)

        for user in chat_users.keys():
            user.send(left_chat_notification)

        print(left_chat_notification)

        chat_users.pop(current_socket)
        current_socket.close()


def manage_message(data, chat_users, current_socket, messages_to_send):
    """
    :param data: data after being parsed using function
    :param chat_users: dictionary that contains {Socket:User}
    :param current_socket: one of connected client's socket
    :param messages_to_send: List of tuples (sender socket, message)
    manages messages server got from users
    """
    if data[MESSAGE_INDEX] == QUITING_MESSAGE:
        close_connection(chat_users, current_socket, False)
        return

    elif data[MESSAGE_INDEX] != EMPTY and chat_users[current_socket] == UNKNOWN_USERNAME:
        update_user(chat_users, current_socket, data)

    else:
        messages_to_send.append((current_socket, data[MESSAGE_INDEX]))


def update_user(chat_users, current_socket, data):
    """
    :param chat_users: dictionary that contains {Socket:User}
    :param current_socket: one of connected client's socket
    :param data: data after being parsed using function
    updates an UNKNOWN user to a new one
    """
    chat_users[current_socket] = ignite_user(data[USERNAME_INDEX])
    if chat_users[current_socket].is_admin:
        current_socket.send(ADMIN_STATUS_NOTIFICATION)


def manage_data(current_socket, chat_users, messages_to_send):
    """
    :param current_socket: one of connected client's socket
    :param chat_users: dictionary that contains {Socket:User}
    :param messages_to_send: List of tuples (sender socket, message)
    """
    data = current_socket.recv(KB)

    if data == EMPTY:
        close_connection(chat_users, current_socket, False)
        return

    data = parse_message(data)

    if data[FUNCTION_INDEX] == MESSAGE_PROTOCOL_CODE:
        manage_message(data, chat_users, current_socket, messages_to_send)

    elif data[FUNCTION_INDEX] == KICK_OUT_CODE:
        close_connection(chat_users, get_key_by_value(chat_users, data[MESSAGE_INDEX]), True)


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