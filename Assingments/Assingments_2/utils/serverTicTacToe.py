import socket
import threading

lobbies = {}

def start_server(port_number):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "localhost"
    port = port_number

    try:
        s.bind((server_ip, port))
    except socket.error as e:
        print(str(e))
        return

    s.listen(5)  # Allow up to 5 connections
    print(f"Server started on port {port_number}")

    while True:
        client_socket, client_address = s.accept()
        print(f"Connection from {client_address} has been established.")
        threading.Thread(target=handle_client, args=(client_socket, client_address, None)).start()

def handle_client(client_socket, client_address, lobby_id):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(f"Received message from {client_address}: {message}")
            if message == 'SHOW_LOBBIES':
                client_socket.sendall(str(lobbies).encode('utf-8'))
            elif message.startswith('CREATE_LOBBY'):
                lobby_name, mode = message.split()[1], message.split()[2]
                board_size = 5 if mode == "blitz" else 3
                lobbies[lobby_name] = {
                    'clients': [client_socket],
                    'board': [['' for _ in range(board_size)] for _ in range(board_size)],
                    'turn': 0,
                    'mode': mode
                }
                client_socket.sendall(f"Lobby {lobby_name} created.".encode('utf-8'))
                print(f"Lobby {lobby_name} created with mode {mode}.")
            elif message.startswith('JOIN_LOBBY'):
                lobby_name = message.split()[1]
                if lobby_name in lobbies:
                    if len(lobbies[lobby_name]['clients']) < 3:
                        lobbies[lobby_name]['clients'].append(client_socket)
                        client_socket.sendall(f"Joined lobby {lobby_name}.".encode('utf-8'))
                        print(f"Client {client_address} joined lobby {lobby_name}.")
                    else:
                        client_socket.sendall("Lobby is full.".encode('utf-8'))
                else:
                    client_socket.sendall("Lobby not found.".encode('utf-8'))
            elif message.startswith('MOVE'):
                lobby_name, move = message.split()[1], message.split()[2]
                if lobby_name in lobbies:
                    i, j, symbol = move.split(',')
                    i, j = int(i), int(j)
                    lobbies[lobby_name]['board'][i][j] = symbol
                    lobbies[lobby_name]['turn'] = (lobbies[lobby_name]['turn'] + 1) % len(lobbies[lobby_name]['clients'])
                    winner = check_winner(lobbies[lobby_name]['board'])
                    for client in lobbies[lobby_name]['clients']:
                        client.sendall(f"MOVE {move}".encode('utf-8'))
                        if winner:
                            client.sendall(f"WINNER {winner}".encode('utf-8'))
                    print(f"Move {move} in lobby {lobby_name}.")
            else:
                client_socket.sendall("Invalid command.".encode('utf-8'))

        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
            break

def check_winner(board):
    size = len(board)
    # Check rows
    for row in board:
        for i in range(size - 3):
            if row[i] == row[i+1] == row[i+2] == row[i+3] != '':
                return row[i]
    # Check columns
    for col in range(size):
        for i in range(size - 3):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col] != '':
                return board[i][col]
    # Check diagonals
    for i in range(size - 3):
        for j in range(size - 3):
            if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] != '':
                return board[i][j]
            if board[i][j+3] == board[i+1][j+2] == board[i+2][j+1] == board[i+3][j] != '':
                return board[i][j+3]
    # Check for tie
    if all(board[i][j] != '' for i in range(size) for j in range(size)):
        return 'Tie'
    return None

if __name__ == "__main__":
    start_server(2341)