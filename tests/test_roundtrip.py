"""
tests/test_roundtrip.py - Testes de ida-e-volta (build → parse)

Garante que um pacote construído pelo builder pode ser interpretado
pelo parser e produz exatamente os mesmos valores originais.
"""

import unittest

from packets.tftp_packets import (
    build_ack,
    build_data,
    build_error,
    build_rrq,
    build_wrq,
    parse_packet,
    OP_ACK,
    OP_DATA,
    OP_ERROR,
    OP_RRQ,
    OP_WRQ,
    BLOCK_SIZE,
)


class TestRoundtrip(unittest.TestCase):

    def test_rrq_roundtrip(self):
        pkt = build_rrq("arquivo.txt", mode="octet")
        result = parse_packet(pkt)
        self.assertEqual(result["opcode"], OP_RRQ)
        self.assertEqual(result["filename"], "arquivo.txt")
        self.assertEqual(result["mode"], "octet")

    def test_wrq_roundtrip(self):
        pkt = build_wrq("upload.bin", mode="octet")
        result = parse_packet(pkt)
        self.assertEqual(result["opcode"], OP_WRQ)
        self.assertEqual(result["filename"], "upload.bin")
        self.assertEqual(result["mode"], "octet")

    def test_data_roundtrip(self):
        payload = b"conteudo do arquivo"
        pkt = build_data(3, payload)
        result = parse_packet(pkt)
        self.assertEqual(result["opcode"], OP_DATA)
        self.assertEqual(result["block_number"], 3)
        self.assertEqual(result["data"], payload)

    def test_data_full_block_roundtrip(self):
        payload = b"A" * BLOCK_SIZE
        pkt = build_data(1, payload)
        result = parse_packet(pkt)
        self.assertEqual(result["data"], payload)

    def test_data_last_block_roundtrip(self):
        """Último bloco (< 512B) também deve fazer o roundtrip."""
        payload = b"fim"
        pkt = build_data(100, payload)
        result = parse_packet(pkt)
        self.assertLess(len(result["data"]), BLOCK_SIZE)
        self.assertEqual(result["data"], payload)

    def test_ack_roundtrip(self):
        pkt = build_ack(7)
        result = parse_packet(pkt)
        self.assertEqual(result["opcode"], OP_ACK)
        self.assertEqual(result["block_number"], 7)

    def test_ack_zero_roundtrip(self):
        pkt = build_ack(0)
        result = parse_packet(pkt)
        self.assertEqual(result["block_number"], 0)

    def test_error_roundtrip_default_msg(self):
        pkt = build_error(1)
        result = parse_packet(pkt)
        self.assertEqual(result["opcode"], OP_ERROR)
        self.assertEqual(result["error_code"], 1)
        self.assertEqual(result["error_msg"], "File not found")

    def test_error_roundtrip_custom_msg(self):
        pkt = build_error(0, "Erro personalizado")
        result = parse_packet(pkt)
        self.assertEqual(result["error_msg"], "Erro personalizado")

    def test_block_number_wraparound(self):
        """Número de bloco 65535 deve fazer o roundtrip sem overflow."""
        pkt = build_data(65535, b"x")
        result = parse_packet(pkt)
        self.assertEqual(result["block_number"], 65535)


if __name__ == "__main__":
    unittest.main()
