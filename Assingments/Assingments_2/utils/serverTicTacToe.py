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
                
                # Set board size based on mode
                if mode == "blitz":
                    board_size = 5  # Blitz mode uses a 5x5 board
                else:
                    board_size = 3  # Default 1v1 mode uses a 3x3 board

                # Create the lobby with the appropriate board size
                lobbies[lobby_name] = {
                    'clients': [client_socket],
                    'board': [['' for _ in range(board_size)] for _ in range(board_size)],
                    'turn': 0,
                    'mode': mode,
                    'board_size': board_size  # Store the board size here
                }
                client_socket.sendall(f"Lobby {lobby_name} created. Board size: {board_size}".encode('utf-8'))
                print(f"Lobby {lobby_name} created with mode {mode}.")

            elif message.startswith('JOIN_LOBBY'):
                lobby_name = message.split()[1]
                if lobby_name in lobbies:
                    if len(lobbies[lobby_name]['clients']) < 3:
                        lobbies[lobby_name]['clients'].append(client_socket)
                        
                        # Send the board size to the new player when they join
                        board_size = lobbies[lobby_name]['board_size']
                        client_socket.sendall(f"Joined lobby {lobby_name}. Board size: {board_size}".encode('utf-8'))
                        print(f"Client {client_address} joined lobby {lobby_name}. Board size: {board_size}")
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
                    
                    # Check for winner after move
                    winner = check_winner(lobbies[lobby_name]['board'])
                    if winner:
                        # Send winner message to all clients in the lobby
                        for client in lobbies[lobby_name]['clients']:
                            client.sendall(f"WINNER {winner}".encode('utf-8'))
                    else:
                        # Continue the game and send the move update
                        for client in lobbies[lobby_name]['clients']:
                            client.sendall(f"MOVE {move}".encode('utf-8'))
                    print(f"Move {move} in lobby {lobby_name}.")

        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
            break


def check_winner(board):
    size = len(board)
    win_condition = 5 if any(lobby['mode'] == 'blitz' for lobby in lobbies.values()) else 3  # 5 in a row for blitz mode

    # Check rows
    for row in board:
        for i in range(size - win_condition + 1):
            if all(cell == row[i] != '' for cell in row[i:i+win_condition]):
                return row[i]
    
    # Check columns
    for col in range(size):
        for i in range(size - win_condition + 1):
            if all(board[row][col] == board[i][col] != '' for row in range(i, i + win_condition)):
                return board[i][col]
    
    # Check diagonals (top-left to bottom-right)
    for i in range(size - win_condition + 1):
        for j in range(size - win_condition + 1):
            if all(board[i+k][j+k] == board[i][j] != '' for k in range(win_condition)):
                return board[i][j]

    # Check diagonals (top-right to bottom-left)
    for i in range(size - win_condition + 1):
        for j in range(win_condition - 1, size):
            if all(board[i+k][j-k] == board[i][j] != '' for k in range(win_condition)):
                return board[i][j]

    # Check for tie
    if all(board[i][j] != '' for i in range(size) for j in range(size)):
        return 'Tie'
    return None


def check_corners(board, symbol):
    size = len(board)
    corners = [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]
    return all(board[i][j] == symbol for i, j in corners)

if __name__ == "__main__":
    start_server(2341)