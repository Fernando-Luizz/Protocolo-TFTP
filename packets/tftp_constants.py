"""
tftp_constants.py - Constantes do protocolo TFTP (RFC 1350).

Este módulo centraliza todos os valores fixos utilizados pelos demais
módulos do pacote TFTP, evitando magic numbers espalhados pelo código.
"""


# Opcodes

OP_RRQ = 1    # Read Request
OP_WRQ = 2    # Write Request
OP_DATA = 3   # Data
OP_ACK = 4    # Acknowledgment
OP_ERROR = 5  # Error


# Parâmetros de transferência

# Tamanho máximo de dados por bloco, conforme RFC 1350
BLOCK_SIZE = 512

# Modos de transferência suportados pelo protocolo
MODE_OCTET = "octet"
MODE_NETASCII = "netascii"

# Códigos e mensagens de erro (RFC 1350, seção 5)

ERROR_CODES = {
    0: "Not defined",
    1: "File not found",
    2: "Access violation",
    3: "Disk full or allocation exceeded",
    4: "Illegal TFTP operation",
    5: "Unknown transfer ID",
    6: "File already exists",
    7: "No such user",
}
