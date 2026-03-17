import socket
import os
import argparse
# 1. Importar o módulo tftp_packets 
from packets.tftp_packets import (
    parse_packet, build_ack, build_data, build_error,
    OP_RRQ, OP_WRQ, BLOCK_SIZE, OP_ACK, OP_DATA
)

def handle_rrq(filename, client_addr):
    """Trata requisições RRQ (Download do cliente)"""
    print(f"[*] RRQ: Enviando '{filename}' para {client_addr}")
    if not os.path.exists(filename):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as err_s:
            err_s.sendto(build_error(1), client_addr)
        return

    # Criar socket efêmero após a requisição inicial
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as transfer_socket:
        #  Controle de timeout e retransmissão simples
        transfer_socket.settimeout(5.0)
        with open(filename, "rb") as f:
            block_num = 1
            while True:
                chunk = f.read(BLOCK_SIZE)
                packet = build_data(block_num, chunk)
                
                for tentativa in range(3):
                    transfer_socket.sendto(packet, client_addr)
                    try:
                        raw_ack, _ = transfer_socket.recvfrom(1024)
                        ack_info = parse_packet(raw_ack)
                        if ack_info['opcode'] == OP_ACK and ack_info['block_number'] == block_num:
                            break
                    except socket.timeout:
                        if tentativa == 2: return # Desiste após 3 tentativas
                
                if len(chunk) < BLOCK_SIZE: break
                block_num = (block_num + 1) % 65536

def handle_wrq(filename, client_addr):
    """Trata requisições WRQ (Upload do cliente)"""
    print(f"[*] WRQ: Recebendo '{filename}' de {client_addr}")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as transfer_socket:
        transfer_socket.settimeout(5.0)
        transfer_socket.sendto(build_ack(0), client_addr) # ACK inicial
        
        with open(filename, "wb") as f:
            expected_block = 1
            while True:
                try:
                    raw_data, addr = transfer_socket.recvfrom(1024)
                    data_info = parse_packet(raw_data)
                    if data_info['opcode'] == OP_DATA and data_info['block_number'] == expected_block:
                        f.write(data_info['data'])
                        transfer_socket.sendto(build_ack(expected_block), addr)
                        if len(data_info['data']) < BLOCK_SIZE: break
                        expected_block = (expected_block + 1) % 65536
                except socket.timeout:
                    return

def start_server():
    # Implementar interface de linha de comando com argparse
    parser = argparse.ArgumentParser(description="Servidor TFTP - Pessoa 3")
    # Permitir porta 69 ou porta alta como 6969
    parser.add_argument("-p", "--port", type=int, default=6969, help="Porta (padrão 6969)")
    parser.add_argument("-d", "--dir", type=str, default=".", help="Diretório base")
    args = parser.parse_args()

    if args.dir != ".":
        if not os.path.exists(args.dir): os.makedirs(args.dir)
        os.chdir(args.dir)

    #  Usar socket UDP para escutar a porta do serviço
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as main_socket:
        main_socket.bind(('0.0.0.0', args.port))
        print(f"[!] Servidor TFTP ativo na porta {args.port}...")

        while True:
            # Tratar requisições RRQ e WRQ
            data, addr = main_socket.recvfrom(1024)
            try:
                info = parse_packet(data)
                if info['opcode'] == OP_RRQ:
                    handle_rrq(info['filename'], addr)
                elif info['opcode'] == OP_WRQ:
                    handle_wrq(info['filename'], addr)
            except Exception as e:
                print(f"[-] Erro ao processar: {e}")

if __name__ == "__main__":
    start_server()
