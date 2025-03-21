import socket

host = '127.0.0.1'
port = 12347

client2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client2_socket.connect((host, port))

definition = client2_socket.recv(1024).decode()
print(definition)

while True:
    game_status = client2_socket.recv(1024).decode()
    print(game_status)

    if "won" in game_status or "lost" in game_status:
        break

    guess = input("Enter a letter: ")
    client2_socket.send(guess.encode())

client2_socket.close()