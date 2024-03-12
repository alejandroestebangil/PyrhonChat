from socket import *
import sys
import threading
from enum import Enum
from colorama import Fore

class Commands(Enum):
    LIST = "/list"
    HELP = "/help"
    CREATE = "/create"
    CONNECT = "/connect"
    JOIN = "/join"
    MSG = "/msg"
    QUIT = "/quit"
    NAME = "/name"
    KICK = "/kick"
    EXIT = "/exit"
    COLOR = "/color"
    MYNAME = "/myname"
    MYCHANNEL = "/mychannel"
    REMOVE = "/remove"

def receive_messages(client_socket, client_name):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                print("Conexión perdida con el servidor.")
                break
            if message.lower().startswith(Commands.HELP.value):
                continue
            if message.startswith("[Mensaje privado"):
                print(Fore.MAGENTA + message + Fore.RESET)
                continue
            parts = message.split(":", 1)
            if len(parts) == 2:
                name, content = parts
                if name != client_name:
                    print(Fore.BLUE + f"{name}:" + Fore.RESET + content)
            else:
                print("", message)
        except ConnectionResetError:
            print("Conexión perdida con el servidor.")
            break
        except ConnectionAbortedError:
            print("")
            break

def main():
    server_ip = "localhost"
    server_port = 9069
    client_name = input("\033[36mIngrese su nombre:\033[0m ")
    client_socket = socket(AF_INET, SOCK_STREAM)
    
    try:
        client_socket.connect((server_ip, server_port))
    except Exception as e:
        print("Error al conectar al servidor:", e)
        sys.exit(1)
    
    client_socket.send(client_name.encode())

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, client_name))
    receive_thread.daemon = True
    receive_thread.start()

    while True:
        user_message = input("")
        if user_message.lower().startswith(Commands.MSG.value):
            parts = user_message.split(" ", 2)
            if len(parts) == 3:
                recipient_name = parts[1]
                private_message = parts[2]
                user_message = f"{Commands.MSG.value} {recipient_name} {private_message}"
            else:
                print("Comando mal formado. Uso: /msg (usuario) (mensaje)\n")
                continue
            
        if user_message.lower().startswith(Commands.NAME.value):
            parts = user_message.split(" ", 1)
            if len(parts) == 2:
                new_name = parts[1]
                user_message = f"{Commands.NAME.value} {new_name}"
                client_name = new_name
            else:
                print("Comando mal formado. Uso: /name (nuevo_nombre)\n")
                continue
            
        if user_message.lower().startswith(Commands.COLOR.value):
            parts = user_message.split(" ", 2)
            if len(parts) == 2:
                color = parts[1]
                user_message = f"{Commands.COLOR.value} {color}"
            else:
                print("Comando mal formado. Uso: /color (color)\n")
                continue
            
        if user_message.lower().startswith(Commands.CREATE.value):
            parts = user_message.split(" ", 1)
            if len(parts) == 2:
                channel_name = parts[1]
                user_message = f"{Commands.CREATE.value} {channel_name}"
            else:
                print("Comando mal formado. Uso: /create (nombre_canal)\n")
                continue
            
        if user_message.lower() == Commands.LIST.value:
            user_message = Commands.LIST.value
            
        if user_message.lower().startswith(Commands.MYNAME.value):
            user_message = Commands.MYNAME.value
            
        elif user_message.lower().startswith(Commands.MYCHANNEL.value):
            user_message = Commands.MYCHANNEL.value
            
        if user_message.lower() == Commands.QUIT.value:
            user_message = Commands.QUIT.value
        
        if user_message.lower() == Commands.EXIT.value:
            client_socket.close()
            receive_thread.join()
            print("Has salido del chat.")
            break
        
        client_socket.send(user_message.encode())

if __name__ == "__main__":
    main()