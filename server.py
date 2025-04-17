import socket
import threading

clients = {}


def broadcast(message, sender_id=None):
    for client_id, client_data in clients.items():
        if client_id != sender_id:
            try:
                client_data['socket'].send(message.encode('utf-8'))
            except:
                pass


def handle_client(client_socket, client_id):
    try:
        # Получаем данные от клиента (имя и IP через разделитель)
        data = client_socket.recv(1024).decode('utf-8').split('|')
        name = data[0]
        custom_ip = data[1]

        clients[client_id] = {
            'socket': client_socket,
            'name': name,
            'ip': custom_ip
        }

        print(f"Клиент {client_id} подключился как {name} ({custom_ip})")
        broadcast(f"{name} ({custom_ip}) присоединился к чату!", client_id)

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message or message == '/exit':
                break
            print(f"{name} ({custom_ip}): {message}")
            broadcast(f"{name} ({custom_ip}): {message}", client_id)

    except Exception as e:
        print(f"Ошибка: {str(e)}")
    finally:
        if client_id in clients:
            print(f"Клиент {client_id} ({name}) отключился")
            broadcast(f"{name} ({custom_ip}) покинул чат", client_id)
            client_socket.close()
            del clients[client_id]


def start_server():
    client_counter = 1

    server_ip = input("Введите IP для сервера: ")
    server_port = int(input("Введите порт для сервера: "))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((server_ip, server_port))
        server_socket.listen(5)
        print(f"Сервер запущен на {server_ip}:{server_port}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Новое подключение от {addr[0]}:{addr[1]}")

            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_counter)
            )
            thread.start()

            client_counter += 1

    except Exception as e:
        print(f"Ошибка сервера: {str(e)}")
    finally:
        server_socket.close()


if __name__ == '__main__':
    start_server()