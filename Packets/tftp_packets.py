"""
tftp_packets.py - Ponto de entrada público do módulo TFTP (RFC 1350).

Este arquivo re-exporta tudo que os demais módulos (server.py, client.py)
precisam importar. A estrutura interna está dividida em:

    tftp_constants.py - opcodes, tamanhos, modos e códigos de erro
    tftp_builders.py - funções build_* para montar pacotes
    tftp_parsers.py  - função parse_packet para interpretar pacotes

Uso:
    from packets.tftp_packets import build_rrq, build_wrq, build_data
    from packets.tftp_packets import build_ack, build_error, parse_packet
    from packets.tftp_packets import OP_RRQ, OP_DATA, BLOCK_SIZE, ERROR_CODES
"""

# Constantes — re-exportadas de tftp_constants

from .tftp_constants import (  # noqa: F401
    BLOCK_SIZE,
    ERROR_CODES,
    MODE_NETASCII,
    MODE_OCTET,
    OP_ACK,
    OP_DATA,
    OP_ERROR,
    OP_RRQ,
    OP_WRQ,
)

# Builders — re-exportados de tftp_builders

from .tftp_builders import (  # noqa: F401
    build_ack,
    build_data,
    build_error,
    build_rrq,
    build_wrq,
)

# Parser — re-exportado de tftp_parsers


from .tftp_parsers import parse_packet  # noqa: F401


# __all__ - define a API pública explicitamente

__all__ = [
    # Opcodes
    "OP_RRQ",
    "OP_WRQ",
    "OP_DATA",
    "OP_ACK",
    "OP_ERROR",
    # Parâmetros
    "BLOCK_SIZE",
    "MODE_OCTET",
    "MODE_NETASCII",
    "ERROR_CODES",
    # Builders
    "build_rrq",
    "build_wrq",
    "build_data",
    "build_ack",
    "build_error",
    # Parser
    "parse_packet",
]
