import socket
import struct

HEADER_SIZE = 4  # 4 byte unsigned int big-endian


def send_frame(sock: socket.socket, message: str) -> None:
    """Kirim satu pesan teks sebagai frame: [4-byte length][payload]."""
    payload = message.encode('utf-8')
    if len(payload) > 0xFFFFFFFF:
        raise ValueError('Payload terlalu besar')
    sock.sendall(struct.pack('!I', len(payload)) + payload)


def recv_exact(sock: socket.socket, n: int) -> bytes:
    """Baca tepat n byte dari socket, atau raise bila koneksi putus."""
    data = b''
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError('Koneksi ditutup sebelum data lengkap diterima')
        data += chunk
    return data


def recv_frame(sock: socket.socket) -> str:
    """Terima satu frame lengkap."""
    raw_len = recv_exact(sock, HEADER_SIZE)
    (payload_len,) = struct.unpack('!I', raw_len)
    payload = recv_exact(sock, payload_len)
    return payload.decode('utf-8')
