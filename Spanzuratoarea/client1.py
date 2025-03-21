import socket

host = '127.0.0.1'
port = 12347

client1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client1_socket.connect((host, port))

word = input("Enter the word to be guessed: ")
definition = input("Enter a definition of the word: ")

client1_socket.send(word.encode())
client1_socket.send(definition.encode())

client1_socket.close()