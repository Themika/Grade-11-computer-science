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
    client_socket.sendall(f"Welcome {player_id} to lobby {lobby_id}! Waiting for your move...\n".encode())
    
    while True:
        try:
            move = client_socket.recv(1024).decode().strip()
            if not move:
                break

            print(f"{player_id} move in lobby {lobby_id}: {move}")
            lobbies[lobby_id]['moves'][player_id] = move

            if len(lobbies[lobby_id]['moves']) == 2:
                player1, player2 = list(lobbies[lobby_id]['moves'].keys())
                move1, move2 = lobbies[lobby_id]['moves'][player1], lobbies[lobby_id]['moves'][player2]
                winner = determine_winner(player1, move1, player2, move2)

                for client, pid in zip(lobbies[lobby_id]['clients'], lobbies[lobby_id]['moves'].keys()):
                    if pid == winner:
                        client.sendall(f"You won! Your move: {move1}. Opponent's move: {move2}.\n".encode())
                    elif winner == "Draw":
                        client.sendall(f"It's a draw! Your move: {move1}. Opponent's move: {move2}.\n".encode())
                    else:
                        client.sendall(f"You lost. Your move: {move1}. Opponent's move: {move2}.\n".encode())

                lobbies[lobby_id]['moves'].clear()

        except ConnectionResetError:
            print(f"{player_id} disconnected from lobby {lobby_id}.")
            break

    client_socket.close()
    lobbies[lobby_id]['clients'].remove(client_socket)
    if not lobbies[lobby_id]['clients']:
        del lobbies[lobby_id]

# Start the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 8765))
    server.listen(5)  # Allow multiple connections
    print("Server started on localhost:8765")

    while True:
        client_socket, client_address = server.accept()
        lobby_id = client_socket.recv(1024).decode().strip()
        if lobby_id not in lobbies:
            lobbies[lobby_id] = {'clients': [], 'moves': {}}
        lobbies[lobby_id]['clients'].append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, client_address, lobby_id)).start()

if __name__ == "__main__":
    start_server()