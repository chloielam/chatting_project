# build a chat server using socket programming
import socket
import threading

# CLIENT[NICKNAME] = [SOCKET, ADDRESS]
CLIENTS = dict()

# create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()
port = 9999

# bind to the port
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))

# listen for clients
server.listen()


def welcome(client_socket):
    # print all existing clients
    client_socket.send('Welcome to the chatroom!\n'.encode('utf-8'))
    client_socket.send('Existing clients: '.encode('utf-8'))
    for nickname in CLIENTS:
        client_socket.send((nickname+" ").encode('utf-8'))
    client_socket.send('\n--------------Start chatting now!\n'.encode('utf-8'))


def private_message(client_socket, nickname, message):
    message = message.decode('utf-8')
    message = message.split(" ", 2)
    if len(message) < 3:
        client_socket.send(
            'Invalid command. Please try again.'.encode('utf-8'))
        return
    if message[1] not in CLIENTS:
        client_socket.send('User not found. Please try again.'.encode('utf-8'))
        return
    send_to_client(CLIENTS[message[1]][0],
                   f'Private {nickname}: {message[2]}')


def send_to_client(client_socket, message):
    client_socket.send(message.encode('utf-8'))


# broadcast messages to all clients
def broadcast(message, nickname, sender=None):
    # notification message
    if sender is None:
        for client_socket, address in CLIENTS.values():
            client_socket.send(message)
    else:
        for client_socket, address in CLIENTS.values():
            if client_socket is not sender:
                client_socket.send(f'{nickname}: '.encode('utf-8') + message)

# handle client messages


def handle(client_socket, nickname):
    while True:
        try:
            # receive message from client
            message = client_socket.recv(1024)
            # private message
            if message.startswith((b'/private')):
                private_message(client_socket, nickname, message)
                continue
            # public message
            broadcast(message, nickname, client_socket)
        except:
            # remove client from CLIENTS
            del CLIENTS[nickname]
            # notify to all clients
            broadcast(f'{nickname} left the chatroom!'.encode(
                'utf-8'), nickname)
            break

# handle new connections


def on_connect(client_socket, address):
    # request and store nickname
    nickname = client_socket.recv(1024).decode('utf-8')
    while nickname in CLIENTS:
        client_socket.send('RESEND_NICK'.encode('utf-8'))
        nickname = client_socket.recv(1024).decode('utf-8')
    # store client information
    CLIENTS[nickname] = (client_socket, address)
    # notify to all clients
    broadcast(f'{nickname} joined the chatroom!'.encode(
        'utf-8'), nickname)
    # welcome new client
    welcome(client_socket)
    # start thread for handling client
    thread = threading.Thread(target=handle, args=(client_socket, nickname))
    thread.start()


# start accepting clients
def accept():
    while True:
        client_socket, address = server.accept()
        print(f'Connected with {str(address)}')
        thread = threading.Thread(
            target=on_connect, args=(client_socket, address))
        thread.start()


if __name__ == '__main__':
    import tkinter as tk
    from tkinter import messagebox
    import sys
    root = tk.Tk()
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
            server.close()
            sys.exit()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Set the window's position
    root.geometry(f"{300}x{100}+{(root.winfo_screenwidth() - 300) // 2}+{(root.winfo_screenheight() - 100) // 2}")
    #set the title
    root.title("SERVER IS ONLINE!")
    
    #display host and port on tkinter windows (centered)
    tk.Label(root, text=f"HOST: {host}").pack(pady=10)
    tk.Label(root, text=f"PORT: {port}").pack(pady=10)

    root.mainloop()

    accept()


    