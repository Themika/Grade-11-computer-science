import socket
import threading

lobbies = {}
# Function to start the server
def start_server(port_number):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "localhost"
    port = port_number
    # Bind the server to the specified port
    try:
        # Bind the server to the specified port
        s.bind((server_ip, port))
    # Handle any errors that occur during the binding process
    except socket.error as e:
        print(str(e))
        return
    # Start listening for incoming connections
    s.listen(5)  
    print(f"Server started on port {port_number}")

    while True:
        # Accept incoming connections
        client_socket, client_address = s.accept()
        print(f"Connection from {client_address} has been established.")
        threading.Thread(target=handle_client, args=(client_socket, client_address, None)).start()

def handle_client(client_socket, client_address, lobby_id):
    while True:
        try:
            # Receive the message from the client
            message = client_socket.recv(1024).decode('utf-8')
            print(f"Received message from {client_address}: {message}")
            # Check if the message is empty
            if message == 'SHOW_LOBBIES':
                client_socket.sendall(str(lobbies).encode('utf-8'))
            # Check if the message is to create a lobby
            elif message.startswith('CREATE_LOBBY'):
                # Extract the lobby name and mode from the message
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
                # Extract the lobby name from the message
                lobby_name = message.split()[1]
                # Check if the lobby exists and is not full
                if lobby_name in lobbies:
                    if len(lobbies[lobby_name]['clients']) < 2:  # Ensure only 2 players for 1v1 mode
                        lobbies[lobby_name]['clients'].append(client_socket)
                        
                        # Send the board size to the new player when they join
                        board_size = lobbies[lobby_name]['board_size']
                        client_socket.sendall(f"BOARD_SIZE {board_size}".encode('utf-8'))
                        print(f"Client {client_address} joined lobby {lobby_name}.")

                        # Notify both players of whose turn it is
                        if len(lobbies[lobby_name]['clients']) == 2:
                            # If both players are in the lobby, inform them
                            current_turn = lobbies[lobby_name]['turn']
                            for index, player in enumerate(lobbies[lobby_name]['clients']):
                                # Send the board to the new player
                                if index == current_turn:
                                    player.sendall("YOUR_TURN".encode('utf-8'))
                                # Send the board to the new player
                                else:
                                    player.sendall("WAIT_FOR_TURN".encode('utf-8'))
                    # If the lobby is full, notify the client
                    else:
                        client_socket.sendall("LOBBY_FULL".encode('utf-8'))
                # If the lobby does not exist, notify the client
                else:
                    client_socket.sendall("LOBBY_NOT_FOUND".encode('utf-8'))


            elif message.startswith('MOVE'):
                # Extract the lobby name and move from the message
                lobby_name, move = message.split()[1], message.split()[2]
                # Check if the lobby exists
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
                            # Notify the clients of whose turn it is
                            if client == lobbies[lobby_name]['clients'][lobbies[lobby_name]['turn']]:
                                client.sendall("YOUR_TURN".encode('utf-8'))
                            # Send the board to the new player
                            else:
                                client.sendall("WAIT_FOR_TURN".encode('utf-8'))
                    print(f"Move {move} in lobby {lobby_name}.")
        # Handle any errors that occur during the message handling process
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
            break
# Function to check for a winner
def check_winner(board):
    size = len(board)
    win_length = 3  # Set win length based on board size

    # Check rows
    for row in board:
        for i in range(size - win_length + 1):
            if all(cell == row[i] != '' for cell in row[i:i+win_length]):
                return row[i]

    # Check columns
    for col in range(size):
        for i in range(size - win_length + 1):
            if all(board[row][col] == board[i][col] != '' for row in range(i, i+win_length)):
                return board[i][col]

    # Check diagonals
    for i in range(size - win_length + 1):
        for j in range(size - win_length + 1):
            if all(board[i+k][j+k] == board[i][j] != '' for k in range(win_length)):
                return board[i][j]
            if all(board[i+k][j+win_length-1-k] == board[i][j+win_length-1] != '' for k in range(win_length)):
                return board[i][j+win_length-1]

    # Check for tie
    if all(board[i][j] != '' for i in range(size) for j in range(size)):
        return 'Tie'
    return None

if __name__ == "__main__":
    start_server(2341)