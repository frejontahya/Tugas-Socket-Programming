#!/usr/bin/env python3
import argparse
import socket
from datetime import datetime


def main() -> None:
    parser = argparse.ArgumentParser(description='UDP heartbeat server')
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=12001)
    args = parser.parse_args()

    # Satu socket UDP tunggal melayani banyak client.
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((args.host, args.port))
        print(f'[UDP] Heartbeat server aktif di {args.host}:{args.port}')
        while True:
            data, client_address = server_socket.recvfrom(65535)
            text = data.decode('utf-8', errors='replace')
            print(f'[UDP] Dari {client_address}: {text}')
            server_socket.sendto(data, client_address)


if __name__ == '__main__':
    main()
