# Hybrid TCP Message Server + UDP Heartbeat/Pinger

Tugas ini mengimplementasikan layanan pesan berbasis TCP konkuren dan layanan heartbeat UDP untuk mengukur RTT serta packet loss.

## Struktur Berkas
- `TCPServer.py` — server TCP multi-thread dengan protokol frame ber-header panjang tetap.
- `TCPClient.py` — client TCP interaktif sederhana untuk mengirim pesan teks.
- `UDPServer.py` — server UDP heartbeat/echo.
- `UDPClient.py` — client UDP pinger 10 kali dengan timeout 1 detik.
- `common.py` — helper protokol `send_frame` dan `recv_frame`.

## Cara Menjalankan
### 1. Nyalakan server
Buka dua terminal terpisah:

```bash
python3 TCPServer.py --host 0.0.0.0 --port 12000
python3 UDPServer.py --host 0.0.0.0 --port 12001
```

### 2. Jalankan client
```bash
python3 UDPClient.py --server 127.0.0.1 --port 12001 --count 10 --timeout 1.0
python3 TCPClient.py --server 127.0.0.1 --port 12000
```

Setelah client TCP terhubung, ketik pesan lalu tekan Enter. Server membalas pesan yang sama dengan awalan `ECHO:`.

## Protokol Aplikasi TCP
Karena TCP adalah byte-stream tanpa batas pesan, aplikasi menggunakan frame:
```text
+----------------------+-------------------+
| 4 byte header length | payload ber-UTF-8 |
+----------------------+-------------------+
```
Header berisi panjang payload dalam byte, dikodekan big-endian unsigned integer. Penerima wajib membaca tepat 4 byte header lalu membaca payload sesuai panjang tersebut.

## Uji Beberapa Client
Jalankan beberapa `TCPClient.py` pada terminal berbeda. Setiap koneksi ditangani thread baru pada server.
