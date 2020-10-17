import socket
import threading
import time

HEADER = 64  # in bytes
FORMAT = 'utf-8'
DISCONNECT_MSG = "!Disconnect"
PORT = 5050  # IMP: Should be the same as that on the server side!
SERVER = "192.168.178.26"  # local IPV4 address
ADDR = (SERVER, PORT)
client_conn_success = 44444  # default non zero return value for client connection status

nickname = input("Enter your chatroom nickname: ")

# these parameters are also the default ones
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_conn_success = client.connect(ADDR)
except socket.error as err:
    print(f"Client not connected due to: {err}")


# Sending messages to server
def send():
    while True:
        try:
            message = f"{nickname}: {input()}"
            client.send(message.encode(FORMAT))

        except socket.error as e:
            print(f"Data cannot be sent or received due to {e}")
            client.close()
            break

# listening to server and Sending messages
def receive():
    while True:
        try:
            # receive messages from server
            incoming_message = client.recv(1024).decode(FORMAT)
            if incoming_message == "UserName: ":
                client.send(nickname.encode(FORMAT))
            else:
                print(incoming_message)
        except socket.error as e:
            print(f"[FATAL ERROR] {e}: Closing client connection..")
            client.close()
            break


if __name__ == "__main__":
    # Starting Threads For Listening And Writing
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    send_thread = threading.Thread(target=send)
    send_thread.start()
