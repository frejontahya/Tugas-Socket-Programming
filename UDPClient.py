#!/usr/bin/env python3
import argparse
import socket
import time


def main() -> None:
    parser = argparse.ArgumentParser(description='UDP pinger client')
    parser.add_argument('--server', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=12001)
    parser.add_argument('--count', type=int, default=10)
    parser.add_argument('--timeout', type=float, default=1.0)
    args = parser.parse_args()

    rtts = []
    lost = 0

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        # Timeout 1 detik untuk menangani paket UDP yang hilang.
        client_socket.settimeout(args.timeout)
        server_address = (args.server, args.port)

        for seq in range(1, args.count + 1):
            send_time = time.time()
            message = f'PING {seq} {send_time}'
            client_socket.sendto(message.encode('utf-8'), server_address)

            try:
                data, _ = client_socket.recvfrom(65535)
                recv_time = time.time()
                rtt_ms = (recv_time - send_time) * 1000
                rtts.append(rtt_ms)
                print(f'#{seq:02d} reply={data.decode()} RTT={rtt_ms:.3f} ms')
            except socket.timeout:
                lost += 1
                print(f'#{seq:02d} request timeout setelah {args.timeout:.1f} detik')

        total = args.count
        loss_percent = (lost / total) * 100 if total else 0.0
        if rtts:
            print('\n=== Ringkasan UDP Pinger ===')
            print(f'Paket terkirim : {total}')
            print(f'Paket diterima : {len(rtts)}')
            print(f'Paket hilang   : {lost} ({loss_percent:.1f}%)')
            print(f'Min RTT        : {min(rtts):.3f} ms')
            print(f'Max RTT        : {max(rtts):.3f} ms')
            print(f'Rata-rata RTT  : {sum(rtts)/len(rtts):.3f} ms')
        else:
            print('\nSemua paket hilang.')


if __name__ == '__main__':
    main()
