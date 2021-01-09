import socket
import threading

host = "127.0.0.1"  # Fill the IPV4 Address of the server.

user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
user_socket.connect((host, 6876))
print(user_socket.recv(1024).decode("utf-8"))
print(user_socket.recv(1024).decode("utf-8"))
user_socket.send(f"{input()}".encode("utf-8"))
Exit = False


def send_message():
    while not Exit:
        try:
            message = input()
            user_socket.send(message.encode("utf-8"))
        except Exception as error:
            print(f"Send Error:{error}")
            break


def listening():
    while True:
        try:
            print(user_socket.recv(1024).decode("utf-8"))
        except Exception as e:
            print(f"Error occurred: {e}")
            break


t1 = threading.Thread(target=listening, daemon=True)
t1.start()
send_message()
