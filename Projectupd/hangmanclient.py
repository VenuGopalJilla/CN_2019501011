
# @author Venu Gopal Jilla

import socket


host = '127.0.0.1'
port = 8888
client_port = (host, port)


def start_information(client_socket):
    login_register = input()
    client_socket.sendall(login_register.encode('utf-8'))
    data = client_socket.recv(1024).decode()
    print(data)
    if data == "Wrong choice":
        return 0


def get_details(client_socket):
    user_name = input()
    client_socket.sendall(user_name.encode('utf-8'))
    data = client_socket.recv(1024).decode()
    print(data)
    if "already present" in data:
        return 0
    password = input()
    client_socket.sendall(password.encode('utf-8'))


def get_letter(client_socket):
    print("entered get_letter")
    get_input ="guesses left"
    game_won = "Congratulations"
    choices_out = "Oops! You lost the game" 
    data = client_socket.recv(1024).decode()
    print(data)
    if get_input in data:
        print("Entered input")
        guessedLetter = input()
        client_socket.sendall(guessedLetter.encode('utf-8'))
    elif game_won in data:
        return 0
    elif choices_out in data:
        return 0
    pass


def client_run():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(client_port)

    data = client_socket.recv(1024).decode()
    print(data)

    ret_val = start_information(client_socket)
    if ret_val == 0:
        client_socket.close()
        return

    ret_val = get_details(client_socket)

    if ret_val == 0:
        client_socket.close()
        return

    data = client_socket.recv(1024).decode()
    if data == "invalid":
        print("invalid user name or password")
        client_socket.close()
        return

    while True:
        ret_val = get_letter(client_socket)
        if ret_val == 0:
            client_socket.close()
            return


client_run()
