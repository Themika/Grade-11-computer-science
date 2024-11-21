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
                lobbies[lobby_name] = {'clients': [client_socket], 'moves': [], 'turn': 0, 'mode': mode}
                client_socket.sendall(f"Lobby {lobby_name} created.".encode('utf-8'))
                print(f"Lobby {lobby_name} created with mode {mode}.")
            elif message.startswith('JOIN_LOBBY'):
                lobby_name = message.split()[1]
                if lobby_name in lobbies:
                    lobbies[lobby_name]['clients'].append(client_socket)
                    client_socket.sendall(f"Joined lobby {lobby_name}.".encode('utf-8'))
                    print(f"Client {client_address} joined lobby {lobby_name}.")
                else:
                    client_socket.sendall("Lobby not found.".encode('utf-8'))
            elif message.startswith('MOVE'):
                lobby_name, move = message.split()[1], message.split()[2]
                if lobby_name in lobbies:
                    lobbies[lobby_name]['moves'].append(move)
                    lobbies[lobby_name]['turn'] = (lobbies[lobby_name]['turn'] + 1) % len(lobbies[lobby_name]['clients'])
                    for client in lobbies[lobby_name]['clients']:
                        client.sendall(f"MOVE {move}".encode('utf-8'))
                    print(f"Move {move} in lobby {lobby_name}.")
            else:
                client_socket.sendall("Invalid command.".encode('utf-8'))
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
            break

if __name__ == "__main__":
    start_server(2341)