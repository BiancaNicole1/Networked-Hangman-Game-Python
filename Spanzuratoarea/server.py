import socket

host = '127.0.0.1'
port = 12347

def draw_hangman(attempts_left):
    stages = [
        """
      _____
     |/   |
     |   ( )
     |   /|\\
     |    |
     |   / \\
     |
     |_____
        """,
        """
      _____
     |/   |
     |   ( )
     |   /|\\
     |    |
     |   / 
     |
     |_____
        """,
        """
      _____
     |/   |
     |   ( )
     |   /|\\
     |    |
     |   
     |
     |_____
        """,
        """
      _____
     |/   |
     |   ( )
     |   /|
     |    |
     |   
     |
     |_____
        """,
        """
      _____
     |/   |
     |   ( )
     |    |
     |    |
     |   
     |
     |_____
        """,
        """
      _____
     |/   |
     |   ( )
     |   
     |    
     |   
     |
     |_____
        """,
        """
      _____
     |/   |
     |   
     |   
     |    
     |   
     |
     |_____
        """
    ]
    return stages[6 - attempts_left]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(2)

print("Waiting for connections...")

client1_conn, addr1 = server_socket.accept()
print(f"Client 1 connected: {addr1}")

client2_conn, addr2 = server_socket.accept()
print(f"Client 2 connected: {addr2}")

word = client1_conn.recv(1024).decode().strip().lower()
definition = client1_conn.recv(1024).decode().strip()

print(f"Word received: {word}")
print(f"Definition received: {definition}")

client2_conn.send(f"Definition: {definition}\n".encode())

hidden_word = ['_'] * len(word)
attempts = 6

while attempts > 0 and '_' in hidden_word:
    hangman_stage = draw_hangman(attempts)
    game_status = f"Word: {' '.join(hidden_word)}   || Attempts left: {attempts}\n{hangman_stage}\n"
    client2_conn.send(game_status.encode())

    guess = client2_conn.recv(1024).decode().strip().lower()

    if guess in word:
        for idx, letter in enumerate(word):
            if letter == guess:
                hidden_word[idx] = guess
    else:
        attempts -= 1

if '_' not in hidden_word:
    client2_conn.send(f"You won! The word was: {word}".encode())
else:
    client2_conn.send(f"You lost! The word was: {word}".encode())

client1_conn.close()
client2_conn.close()
server_socket.close()