import json
import socket


def connect():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.0.104', 8080))
    return client_socket


def update_balance(user):
    client_socket = connect()

    email = user.get('email')
    balance = user.get('balance')

    data = {}
    data['email'] = email
    data['balance'] = balance
    data_str = json.dumps(data)

    client_socket.send(f"balance {data_str}\n".encode())
    client_socket.close()


# Пример использования функции register_user

