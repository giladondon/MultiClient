import socket
import select

__author__ = 'Gilad Barak'

PORT = 23
SELF_ASSIGN_SERVER = '0.0.0.0'
NUMBER_OF_LISTENING = 5
KB = 1024
EMPTY = ''


def send_waiting_messages(write_list, messages_to_send):
    """
    :param write_list: Sockets available to write to
    :param messages_to_send: List of tuples (sender socket, message)
    Sends data to all chat users except the sender and clears list
    """
    for message in messages_to_send:
        (client_socket, data) = message
        for user in write_list:
            if user is not client_socket:
                user.send(data)
        print(data)
        messages_to_send.remove(message)


def main():
    server_socket = socket.socket()
    server_socket.bind((SELF_ASSIGN_SERVER, PORT))
    server_socket.listen(NUMBER_OF_LISTENING)
    open_client_sockets = []
    messages_to_send = []
    while True:
        read_list, write_list, error_list = select.select([server_socket] + open_client_sockets,
                                                          open_client_sockets, [])
        for current_socket in read_list:
            if current_socket is server_socket:
                (new_socket, address) = current_socket.accept()
                open_client_sockets.append(new_socket)
            else:
                data = current_socket.recv(KB)
                if data == EMPTY:
                    open_client_sockets.remove(current_socket)
                    print('Someone closed connection')
                else:
                    messages_to_send.append((current_socket, data))
        send_waiting_messages(write_list, messages_to_send)

if __name__ == '__main__':
    main()