"""
tftp_builders.py - Funções de construção de pacotes TFTP (RFC 1350).

Cada função recebe parâmetros de alto nível e devolve os bytes prontos
para envio via socket UDP.

Funções públicas:
    build_rrq - Read Request  (opcode 1)
    build_wrq - Write Request (opcode 2)
    build_data - Data          (opcode 3)
    build_ack - Acknowledge   (opcode 4)
    build_error - Error         (opcode 5)
"""

import struct

from tftp_constants import (
    BLOCK_SIZE,
    ERROR_CODES,
    MODE_OCTET,
    OP_ACK,
    OP_DATA,
    OP_ERROR,
    OP_RRQ,
    OP_WRQ,
)

# Funções públicas

def build_rrq(filename: str, mode: str = MODE_OCTET) -> bytes:
    """Constrói um pacote RRQ (Read Request).

    Formato:
        | opcode (2B) | filename (str\\0) | mode (str\\0) |

    Args:
        filename: Nome do arquivo a ser lido no servidor.
        mode:     Modo de transferência ("octet" ou "netascii").
                  Padrão: "octet".

    Returns:
        Bytes do pacote RRQ pronto para envio via UDP.

    Raises:
        ValueError: Se filename ou mode estiverem vazios.

    Exemplo:
        >>> pkt = build_rrq("foto.png")
        >>> len(pkt) > 0
        True
    """
    _validate_request_args(filename, mode)
    return _build_request(OP_RRQ, filename, mode)


def build_wrq(filename: str, mode: str = MODE_OCTET) -> bytes:
    """Constrói um pacote WRQ (Write Request).

    Formato:
        | opcode (2B) | filename (str\\0) | mode (str\\0) |

    Args:
        filename: Nome do arquivo a ser escrito no servidor.
        mode:     Modo de transferência ("octet" ou "netascii").
                  Padrão: "octet".

    Returns:
        Bytes do pacote WRQ pronto para envio via UDP.

    Raises:
        ValueError: Se filename ou mode estiverem vazios.

    Exemplo:
        >>> pkt = build_wrq("relatorio.pdf")
        >>> len(pkt) > 0
        True
    """
    _validate_request_args(filename, mode)
    return _build_request(OP_WRQ, filename, mode)


def build_data(block_number: int, data: bytes) -> bytes:
    """Constrói um pacote DATA.

    Formato:
        | opcode (2B) | block# (2B) | data (até 512B) |

    Um bloco com menos de 512 bytes sinaliza o fim da transferência.

    Args:
        block_number: Número sequencial do bloco (1 a 65535).
        data:         Bytes de dados a enviar (máximo BLOCK_SIZE bytes).

    Returns:
        Bytes do pacote DATA pronto para envio via UDP.

    Raises:
        ValueError: Se block_number estiver fora do intervalo válido ou
                    se data exceder BLOCK_SIZE bytes.

    Exemplo:
        >>> pkt = build_data(1, b"hello")
        >>> len(pkt)
        9
    """
    if not (1 <= block_number <= 65535):
        raise ValueError(
            f"block_number deve estar entre 1 e 65535, recebido: {block_number}"
        )
    if len(data) > BLOCK_SIZE:
        raise ValueError(
            f"data excede o tamanho máximo de {BLOCK_SIZE} bytes "
            f"(recebido {len(data)} bytes)"
        )
    return struct.pack("!HH", OP_DATA, block_number) + data


def build_ack(block_number: int) -> bytes:
    """Constrói um pacote ACK (Acknowledgment).

    Formato:
        | opcode (2B) | block# (2B) |

    O ACK do WRQ inicial usa block_number = 0.

    Args:
        block_number: Número do bloco confirmado (0 a 65535).

    Returns:
        Bytes do pacote ACK pronto para envio via UDP.

    Raises:
        ValueError: Se block_number estiver fora do intervalo válido.

    Exemplo:
        >>> pkt = build_ack(0)
        >>> len(pkt)
        4
    """
    if not (0 <= block_number <= 65535):
        raise ValueError(
            f"block_number deve estar entre 0 e 65535, recebido: {block_number}"
        )
    return struct.pack("!HH", OP_ACK, block_number)


def build_error(error_code: int, error_msg: str = "") -> bytes:
    """Constrói um pacote ERROR.

    Formato:
        | opcode (2B) | errorcode (2B) | errmsg (str\\0) |

    Se error_msg não for fornecido, usa a mensagem padrão do código.

    Args:
        error_code: Código de erro conforme RFC 1350 (0 a 7).
        error_msg:  Mensagem de erro legível. Se vazio, usa ERROR_CODES.

    Returns:
        Bytes do pacote ERROR pronto para envio via UDP.

    Raises:
        ValueError: Se error_code estiver fora do intervalo 0–7.

    Exemplo:
        >>> pkt = build_error(1)
        >>> len(pkt) > 4
        True
    """
    if not (0 <= error_code <= 7):
        raise ValueError(
            f"error_code deve estar entre 0 e 7, recebido: {error_code}"
        )
    if not error_msg:
        error_msg = ERROR_CODES.get(error_code, "Unknown error")
    msg_encoded = error_msg.encode("ascii") + b"\x00"
    return struct.pack("!HH", OP_ERROR, error_code) + msg_encoded



# Funções auxiliares privadas

def _validate_request_args(filename: str, mode: str) -> None:
    """Valida os argumentos comuns de RRQ e WRQ."""
    if not filename:
        raise ValueError("filename não pode ser vazio.")
    if not mode:
        raise ValueError("mode não pode ser vazio.")


def _build_request(opcode: int, filename: str, mode: str) -> bytes:
    """Monta o payload binário de um pacote RRQ ou WRQ."""
    filename_encoded = filename.encode("ascii") + b"\x00"
    mode_encoded = mode.encode("ascii") + b"\x00"
    return struct.pack("!H", opcode) + filename_encoded + mode_encoded
