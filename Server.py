import socket
import threading
import sys

clients = []
nicknames = []
members = {}
print("***********Setting up server************")
server_type = input("Choose the type of server...\n1.)Offline Server\n2.)Online Server\n")

if server_type == "1":
    server_type = "127.0.0.1"
elif server_type == "2":
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.connect(("8.8.8.8", 80))  # Google DNS - For your IPV4 Address.
        server_type = server.getsockname()[0]
        server.close()
    except Exception as online_error:
        print(f"{online_error}: Check your internet connection.")
        sys.exit()
else:
    print("Invalid option !")
    sys.exit()
print("For Master Control login create an Admin account...")
Admin_name = input("\nCreate Admin name: ")  # Create a Admin account for master control.
password = input("Create Password: ")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_type, 6876))
server.listen(5)


def master_control(client, nickname):  # For Admin use
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message.startswith("//"):
                if "//kick" in message:  # Use "//kick %client's nickname% to remove them from chat."
                    message = message.replace("//kick ", "")
                    if message in nicknames:
                        kicked_id = members.get(message)
                        kicked_id.send(f"Admin/{nickname} has removed you from Chat.".encode("utf-8"))
                        clients.remove(kicked_id)
                        members.pop(message)
                        kicked_id.close()
                        nicknames.remove(message)
                        send_all(f"{nickname} has removed {message} from chat.")
                    else:
                        client.send(f"No such person named {message}.".encode("utf-8"))

                elif "//clients" in message:  # Use "//clients" to see all information of clients and their nickname.
                    client.send(str(clients).encode("utf-8"))
                    client.send(str(nicknames).encode("utf-8"))
                    client.send(str(members).encode("utf-8"))
            else:
                send_all(f"{nickname}: {message}")
        except Exception as master_error:
            print(f"master_error: {master_error}")
            send_all(f"Admin/{nickname} has left the chat.")
            break
        continue
    return None


def send_all(message):
    for client in clients:
        try:
            client.send(message.encode("utf-8"))
        except Exception as pass_error:
            print(f"send_all error: {pass_error}")
            continue


def accept_client():  # Accepts connections.
    while True:
        client, address = server.accept()
        clients.append(client)
        client.send("***************Welcome to the Server*****************".encode("utf-8"))
        client_thread = threading.Thread(target=handle_client, args=(client,))
        client_thread.start()


def nickname_client(client):  # Verify if the person connected is Admin or normal client.
    try:
        client.send("\nChoose a nickname: ".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")
        if nickname.startswith("//") and len(nickname) > 2:
            nickname = nickname.replace("//", "")
            if nickname == Admin_name:
                client.send("Enter Password: ".encode("utf-8"))
                passcode = client.recv(1024).decode("utf-8")
                if passcode == password:
                    client.send("ACCESS GRANTED".encode("utf-8"))
                    members.update({nickname: client})
                    send_all(f"Admin/{nickname} has joined the chat.")
                    master_control(client, nickname)

                else:
                    client.send("ACCESS DENIED".encode("utf-8"))
    except Exception as connection_error:
        print(f"Connection error: {connection_error}")
        clients.remove(client)
        client.close()
        return None
    return nickname


def handle_client(client):  # MAIN FUNCTION>>To handle Admin and clients.
    try:
        nickname = nickname_client(client)
        if client in clients:
            while nickname in nicknames or nickname == Admin_name:
                client.send("This nickname is not available. Choose another one.".encode("utf-8"))
                nickname = nickname_client(client)
            nicknames.append(nickname)
            if nickname is not None:
                send_all(f"{nickname} has joined the chat.")
            members.update({nickname: client})
            while True:
                try:
                    message = client.recv(1024).decode("utf-8")
                    send_all(f"{nickname}: {message}")
                except Exception as sending_error:
                    print(f"sending error: {sending_error}")
                    if client in clients:
                        clients.remove(client)
                    nicknames.remove(nickname)
                    members.pop(nickname)
                    if nickname is not None:
                        send_all(f"{nickname} has left the chat.")
                    break
        else:
            print("Client can not be found!")
    except Exception as handling_error:
        print(f"handling error: {handling_error}")
        if client in clients:
            clients.remove(client)
    return None


print(f"Server is Online:\nClients can connect through this IPV4 address--\n{server_type}")
accept_client()
