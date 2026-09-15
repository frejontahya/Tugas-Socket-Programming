#!/usr/bin/env python3
import argparse
import socket
import threading
from datetime import datetime

from common import send_frame, recv_frame


def handle_client(connection_socket: socket.socket, client_address, client_id: int) -> None:
    print(f'[TCP] Client {client_id} terhubung dari {client_address}')
    try:
        while True:
            message = recv_frame(connection_socket)
            print(f'[TCP] Client {client_id}: {message}')
            response = f'ECHO: {message}'
            send_frame(connection_socket, response)
    except (ConnectionError, OSError):
        pass
    finally:
        connection_socket.close()
        print(f'[TCP] Client {client_id} dari {client_address} terputus')


def main() -> None:
    parser = argparse.ArgumentParser(description='TCP multi-threaded echo server')
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=12000)
    args = parser.parse_args()

    # Welcoming socket: dipakai hanya untuk listen() dan accept(), bukan untuk bertukar data aplikasi.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((args.host, args.port))
        server_socket.listen(100)
        print(f'[TCP] Server aktif di {args.host}:{args.port}')

        next_client_id = 1
        while True:
            # connection_socket: socket khusus untuk satu client yang baru diterima.
            connection_socket, client_address = server_socket.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(connection_socket, client_address, next_client_id),
                daemon=True
            )
            thread.start()
            next_client_id += 1


if __name__ == '__main__':
    main()
