import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            print("Соединение с сервером разорвано")
            break


def start_client():
    server_ip = input("Введите IP сервера: ")
    server_port = int(input("Введите порт сервера: "))

    name = input("Введите ваше имя: ")
    custom_ip = input("Введите ваш IP: ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_ip, server_port))

        client_socket.send(f"{name}|{custom_ip}".encode('utf-8'))

        print(f"Подключено как {name} ({custom_ip})")

        receive_thread = threading.Thread(
            target=receive_messages,
            args=(client_socket,)
        )
        receive_thread.start()

        while True:
            message = input()
            if message.lower() == '/exit':
                client_socket.send('/exit'.encode('utf-8'))
                break
            client_socket.send(message.encode('utf-8'))

    except Exception as e:
        print(f"Ошибка: {str(e)}")
    finally:
        client_socket.close()
        print("Соединение закрыто")


if __name__ == '__main__':
    start_client()