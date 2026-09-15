#!/usr/bin/env python3
import argparse
import socket

from common import send_frame, recv_frame


def main() -> None:
    parser = argparse.ArgumentParser(description='TCP frame client')
    parser.add_argument('--server', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=12000)
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((args.server, args.port))
        print(f'Terhubung ke {args.server}:{args.port}. Ketik pesan, atau "exit" untuk keluar.')
        while True:
            try:
                message = input('> ')
            except (EOFError, KeyboardInterrupt):
                break
            if message.strip().lower() == 'exit':
                break
            send_frame(client_socket, message)
            reply = recv_frame(client_socket)
            print(reply)


if __name__ == '__main__':
    main()
