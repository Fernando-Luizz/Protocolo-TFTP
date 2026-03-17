"""
tftp_parsers.py — Interpretação de pacotes TFTP brutos (RFC 1350).

Recebe bytes vindos do socket UDP e devolve dicionários com os campos
de cada tipo de pacote.

Funções públicas:
    parse_packet - despacha para o parser correto conforme o opcode
"""

import struct

from .tftp_constants import (
    OP_ACK,
    OP_DATA,
    OP_ERROR,
    OP_RRQ,
    OP_WRQ,
)


# Função pública


def parse_packet(packet: bytes) -> dict:
    """Interpreta um pacote TFTP bruto e retorna seus campos em um dicionário.

    O campo "opcode" estará sempre presente. Os demais campos dependem
    do tipo de pacote:

        RRQ / WRQ  → {"opcode", "filename", "mode"}
        DATA       → {"opcode", "block_number", "data"}
        ACK        → {"opcode", "block_number"}
        ERROR      → {"opcode", "error_code", "error_msg"}

    Args:
        packet: Bytes brutos recebidos via UDP.

    Returns:
        Dicionário com os campos do pacote interpretado.

    Raises:
        ValueError: Se o pacote for curto demais ou tiver opcode inválido.

    Exemplo:
        >>> from packets.tftp_packets import build_ack
        >>> raw = build_ack(3)
        >>> parse_packet(raw)
        {'opcode': 4, 'block_number': 3}
    """
    if len(packet) < 2:
        raise ValueError("Pacote muito curto: mínimo de 2 bytes esperado.")

    (opcode,) = struct.unpack("!H", packet[:2])

    _parsers = {
        OP_RRQ: _parse_request,
        OP_WRQ: _parse_request,
        OP_DATA: _parse_data,
        OP_ACK: _parse_ack,
        OP_ERROR: _parse_error,
    }

    parser = _parsers.get(opcode)
    if parser is None:
        raise ValueError(f"Opcode desconhecido: {opcode}")

    return parser(opcode, packet)


# Funções auxiliares privadas

def _parse_request(opcode: int, packet: bytes) -> dict:
    """Interpreta um pacote RRQ ou WRQ."""
    payload = packet[2:]
    parts = payload.split(b"\x00")

    if len(parts) < 2:
        raise ValueError("Pacote RRQ/WRQ malformado: campos insuficientes.")

    filename = parts[0].decode("ascii")
    mode = parts[1].decode("ascii")

    if not filename:
        raise ValueError("Pacote RRQ/WRQ malformado: filename vazio.")
    if not mode:
        raise ValueError("Pacote RRQ/WRQ malformado: mode vazio.")

    return {
        "opcode": opcode,
        "filename": filename,
        "mode": mode,
    }


def _parse_data(opcode: int, packet: bytes) -> dict:
    """Interpreta um pacote DATA."""
    if len(packet) < 4:
        raise ValueError("Pacote DATA malformado: mínimo de 4 bytes esperado.")

    _, block_number = struct.unpack("!HH", packet[:4])

    return {
        "opcode": OP_DATA,
        "block_number": block_number,
        "data": packet[4:],
    }


def _parse_ack(opcode: int, packet: bytes) -> dict:
    """Interpreta um pacote ACK."""
    if len(packet) < 4:
        raise ValueError("Pacote ACK malformado: mínimo de 4 bytes esperado.")

    _, block_number = struct.unpack("!HH", packet[:4])

    return {
        "opcode": OP_ACK,
        "block_number": block_number,
    }


def _parse_error(opcode: int, packet: bytes) -> dict:
    """Interpreta um pacote ERROR."""
    if len(packet) < 5:
        raise ValueError(
            "Pacote ERROR malformado: mínimo de 5 bytes esperado."
        )

    _, error_code = struct.unpack("!HH", packet[:4])
    error_msg = packet[4:].rstrip(b"\x00").decode("ascii", errors="replace")

    return {
        "opcode": OP_ERROR,
        "error_code": error_code,
        "error_msg": error_msg,
    }
