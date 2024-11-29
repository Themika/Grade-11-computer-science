# FILE: serverRPS.py

import socket
import threading

# Global variables to track lobbies
lobbies = {}

# Determine winner function
def determine_winner(player1, move1, player2, move2):
    outcomes = {
        "Rock": {"Rock": "Draw", "Paper": player2, "Scissors": player1},
        "Paper": {"Rock": player1, "Paper": "Draw", "Scissors": player2},
        "Scissors": {"Rock": player2, "Paper": player1, "Scissors": "Draw"},
    }
    return outcomes[move1][move2]

# Handle client communication
def handle_client(client_socket, client_address, lobby_id):
    player_id = f"Player{len(lobbies[lobby_id]['clients'])}"
    print(f"{player_id} connected to lobby {lobby_id}: {client_address}")
    client_socket.sendall(f"Welcome {player_id} to lobby {lobby_id}!\n\t Waiting for your move...".encode())
    
    while True:
        try:
            # Receive the move from the client
            move = client_socket.recv(1024).decode().strip()
            if not move:
                break

            print(f"{player_id} move in lobby {lobby_id}: {move}")
            lobbies[lobby_id]['moves'][player_id] = move
            # If both players have made a move, determine the winner
            if len(lobbies[lobby_id]['moves']) == 2:
                player1, player2 = list(lobbies[lobby_id]['moves'].keys())
                move1, move2 = lobbies[lobby_id]['moves'][player1], lobbies[lobby_id]['moves'][player2]
                winner = determine_winner(player1, move1, player2, move2)
                # Notify the clients of the result
                for client, pid in zip(lobbies[lobby_id]['clients'], lobbies[lobby_id]['moves'].keys()):
                    result = "won" if pid == winner else "lost" if winner != "Draw" else "draw"
                    client.sendall(f"You {result}! Your move: {move1}.\n Opponent's move: {move2}".encode())

                lobbies[lobby_id]['moves'].clear()

        except ConnectionResetError:
            # Handle client disconnection
            print(f"{player_id} disconnected from lobby {lobby_id}.")
            break
    # Remove the client from the lobby
    client_socket.close()
    lobbies[lobby_id]['clients'].remove(client_socket)
    if not lobbies[lobby_id]['clients']:
        del lobbies[lobby_id]

# Start the server
def start_server(server_number):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", server_number))
    server.listen(5)  # Allow multiple connections
    print(f"Server started on localhost:{server_number}")

    while True:
        # Accept incoming connections
        client_socket, client_address = server.accept()
        lobby_id = client_socket.recv(1024).decode().strip()
        # Create a new lobby if the client requests it
        if lobby_id.startswith("CREATE_LOBBY"):
            lobby_id = lobby_id.split()[1]
            # Check if the lobby already exists
            if lobby_id not in lobbies:
                lobbies[lobby_id] = {'clients': [client_socket], 'moves': {}}
                client_socket.sendall(f"LOBBY_CREATED {lobby_id}".encode('utf-8'))
                threading.Thread(target=handle_client, args=(client_socket, client_address, lobby_id)).start()
            # If the lobby already exists, add the client to it
            else:
                client_socket.sendall("LOBBY_EXISTS".encode('utf-8'))
                client_socket.close()
        # Add the client to an existing lobby
        elif lobby_id not in lobbies:
            client_socket.sendall("LOBBY_NOT_FOUND".encode('utf-8'))
            client_socket.close()
        # Add the client to the existing lobby
        else:
            lobbies[lobby_id]['clients'].append(client_socket)
            threading.Thread(target=handle_client, args=(client_socket, client_address, lobby_id)).start()

if __name__ == "__main__":
    start_server(8765)