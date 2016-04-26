import socket
import select

__author__ = 'Gilad Barak'

PORT = 23
SELF_ASSIGN_SERVER = '0.0.0.0'
NUMBER_OF_LISTENING = 5
KB = 1024
EMPTY = ''


def send_waiting_messages(write_list, messages_to_send):
    for message in messages_to_send:
        (client_socket, data) = message
        if client_socket in write_list:
            client_socket.send(data)
            messages_to_send.remove(message)


def main():
    server_socket = socket.socket()
    server_socket.bind((SELF_ASSIGN_SERVER, PORT))
    server_socket.listen(NUMBER_OF_LISTENING)
    open_client_sockets = []
    messages_to_send = []
    while True:
        read_list, write_list, error_list = select.select([server_socket] + open_client_sockets, open_client_sockets, [])
        for current_socket in read_list:
            if current_socket is server_socket:
                (new_socket, address) = current_socket.accept()
                open_client_sockets.append(new_socket)
            else:
                data = current_socket.recv(KB)
                if data == EMPTY:
                    open_client_sockets.remove(current_socket)
                    print('Client closed connection')
                else:
                    messages_to_send.append((current_socket, 'Hello, ' + data))
        send_waiting_messages(write_list, messages_to_send)

if __name__ == '__main__':
    main()