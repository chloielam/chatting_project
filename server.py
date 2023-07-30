import socket
import threading
import ctypes
from sortedcontainers import SortedDict
import re
# CLIENT[NICKNAME] = [SOCKET, ADDRESS]
# {bytes: [socket.socket, (str, int)]}
CLIENTS = SortedDict()

# create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allow reuse of address

# get local machine name
host = socket.gethostname()
port = 9999


# bind to the port
# allow only one instance of the server to run
try:
    server.bind((host, port))
except:
    ctypes.windll.user32.MessageBoxW(
        0, "Another instance of the server is already running!", "Error", 1)
    sys.exit(0)
# listen for clients
server.listen()

# send welcome message to new client


def welcome(client_socket) -> None:
    send_to_client(
        client_socket, '                              ------   Welcome to the chatroom!   ------                             \n')
    send_to_client(
        client_socket, '                                ------   Type /help for more info.   ------                             \n')


def private_message(client_socket, nickname, message) -> None:
    structure = re.compile(r'^(/private)\s(\(.{2,16}\))\s(.+)$')
    _, receiver, text = structure.match(message.decode('utf-8')).groups()
    lookup_nickname = receiver[1:-1].encode('utf-8')
    if lookup_nickname not in CLIENTS:
        client_socket.send(
            '————> User not found. Please try again.'.encode('utf-8'))
        return
    display_nickname = nickname.decode('utf-8')
    send_to_client(CLIENTS[lookup_nickname][0],
                   f'[Private from {display_nickname}]: {text}')


def send_to_client(client_socket, message):
    client_socket.send(message.encode('utf-8'))


# broadcast messages to all clients


def broadcast(message, nickname, sender=None) -> None:
    # notification message
    if sender is None or nickname == "SERVER":
        notification = (85-len(message))//2 * ' '  \
            + '-'*6 + "   " + message + "   " + '-' * \
            6 + (85-len(message))//2 * ' '+'\n'
        notification = notification.encode('utf-8')
        for client_socket, address in CLIENTS.values():
            client_socket.send(notification)
    else:
        for client_socket, address in CLIENTS.values():
            if client_socket is not sender:
                display_nickname = nickname.decode('utf-8')
                client_socket.send(
                    f'[{display_nickname}]: '.encode('utf-8') + message)

# handle client messages


def handle(client_socket, nickname) -> None:
    while True:
        try:
            # receive message from client
            message = client_socket.recv(1024)
            # private message
            if message.startswith((b'/private')):
                private_message(client_socket, nickname, message)
                continue
            # public message- broadcast to all clients
            broadcast(message, nickname, client_socket)
        except:
            # remove client from CLIENTS
            del CLIENTS[nickname]
            # notify to all clients
            broadcast(f'{nickname} left the chatroom!', "SERVER")
            break


# handle new connections


def on_connect(client_socket, address: tuple) -> None:
    # request and store nickname
    try:
        storing_nickname = client_socket.recv(1024)  # bytes
        display_nickname = storing_nickname.decode('utf-8')  # string

        # check if nickname is already taken
        while storing_nickname in CLIENTS:
            client_socket.send(
                'RESEND_NICK'.encode('utf-8'))
            storing_nickname = client_socket.recv(1024)
            display_nickname = storing_nickname.decode('utf-8')

        # store client information
        CLIENTS[storing_nickname] = (client_socket, address)
        # notify to all clients
        broadcast(f'{display_nickname} joined the chatroom!', "SERVER")
        # welcome new client
        welcome(client_socket)
        # start thread for handling client
        thread = threading.Thread(
            target=handle, args=(client_socket, storing_nickname))
        thread.start()
    except:
        return

# start accepting clients


def accept() -> None:
    while True:
        try:
            client_socket, address = server.accept()
            print(f'Connected with {str(address)}')
            thread = threading.Thread(
                target=on_connect, args=(client_socket, address))
            thread.start()
        except:
            break


if __name__ == '__main__':
    import tkinter as tk
    from tkinter import messagebox
    import sys

    root = tk.Tk()

    def on_closing():
        root.destroy()
        server.close()
        sys.exit(0)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Set the window's position
    root.geometry(
        f"{300}x{100}+{(root.winfo_screenwidth() - 300) // 2}+{(root.winfo_screenheight() - 100) // 2}")
    # set the title
    root.title("SERVER IS ONLINE!")
    root.resizable(False, False)
    # display host and port on tkinter windows (centered)
    tk.Label(root, text=f"HOST: {host}").pack(pady=10)
    tk.Label(root, text=f"PORT: {port}").pack(pady=10)

    # start accepting clients
    accept_thread = threading.Thread(target=accept)
    accept_thread.start()
    root.mainloop()
