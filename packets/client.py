import socket
import argparse

from packets.tftp_packets import (
    build_rrq,
    build_wrq,
    build_ack,
    build_data,
    parse_packet,
    OP_DATA,
    OP_ACK,
    OP_ERROR,
    BLOCK_SIZE,
)

TIMEOUT = 5


def download_file(server_ip, server_port, filename):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)

    rrq = build_rrq(filename)
    sock.sendto(rrq, (server_ip, server_port))

    file_data = b""
    expected_block = 1

    print(f"[INFO] Baixando {filename}...")

    while True:
        try:
            data, addr = sock.recvfrom(516)
        except socket.timeout:
            print("[ERRO] Timeout durante download")
            return

        packet = parse_packet(data)

        if packet["opcode"] == OP_DATA:
            block = packet["block_number"]
            payload = packet["data"]

            if block == expected_block:
                file_data += payload

                ack = build_ack(block)
                sock.sendto(ack, addr)

                expected_block += 1

                # fim do arquivo
                if len(payload) < BLOCK_SIZE:
                    break

        elif packet["opcode"] == OP_ERROR:
            print(f"[ERRO] {packet['error_msg']}")
            return

    with open(filename, "wb") as f:
        f.write(file_data)

    print("[OK] Download concluído")


def upload_file(server_ip, server_port, filename):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)

    try:
        file = open(filename, "rb")
    except FileNotFoundError:
        print("[ERRO] Arquivo não encontrado")
        return

    wrq = build_wrq(filename)
    sock.sendto(wrq, (server_ip, server_port))

    print(f"[INFO] Enviando {filename}...")

    block_number = 0

    while True:
        try:
            data, addr = sock.recvfrom(516)
        except socket.timeout:
            print("[ERRO] Timeout durante upload")
            return

        packet = parse_packet(data)

        if packet["opcode"] == OP_ACK:
            ack_block = packet["block_number"]

            if ack_block == block_number:
                chunk = file.read(BLOCK_SIZE)
                block_number += 1

                data_pkt = build_data(block_number, chunk)
                sock.sendto(data_pkt, addr)

                if len(chunk) < BLOCK_SIZE:
                    break

        elif packet["opcode"] == OP_ERROR:
            print(f"[ERRO] {packet['error_msg']}")
            return

    file.close()
    print("[OK] Upload concluído")


def main():
    parser = argparse.ArgumentParser(description="Cliente TFTP")

    parser.add_argument("operation", choices=["get", "put"])
    parser.add_argument("filename")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=69)

    args = parser.parse_args()

    if args.operation == "get":
        download_file(args.host, args.port, args.filename)
    elif args.operation == "put":
        upload_file(args.host, args.port, args.filename)


if __name__ == "__main__":
    main()