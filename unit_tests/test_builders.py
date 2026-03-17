"""
tests/test_builders.py - Testes unitários para packets/tftp_builders.py

Cobre a construção correta de cada tipo de pacote TFTP e a validação
dos argumentos inválidos.
"""

import struct
import unittest

from packets.tftp_packets import (
    build_ack,
    build_data,
    build_error,
    build_rrq,
    build_wrq,
    OP_ACK,
    OP_DATA,
    OP_ERROR,
    OP_RRQ,
    OP_WRQ,
    BLOCK_SIZE,
)


class TestBuildRrq(unittest.TestCase):

    def test_opcode_is_rrq(self):
        pkt = build_rrq("file.txt")
        opcode, = struct.unpack("!H", pkt[:2])
        self.assertEqual(opcode, OP_RRQ)

    def test_filename_in_packet(self):
        pkt = build_rrq("foto.png")
        self.assertIn(b"foto.png\x00", pkt)

    def test_default_mode_is_octet(self):
        pkt = build_rrq("file.txt")
        self.assertIn(b"octet\x00", pkt)

    def test_custom_mode_netascii(self):
        pkt = build_rrq("file.txt", mode="netascii")
        self.assertIn(b"netascii\x00", pkt)

    def test_empty_filename_raises(self):
        with self.assertRaises(ValueError):
            build_rrq("")

    def test_empty_mode_raises(self):
        with self.assertRaises(ValueError):
            build_rrq("file.txt", mode="")


class TestBuildWrq(unittest.TestCase):

    def test_opcode_is_wrq(self):
        pkt = build_wrq("file.txt")
        opcode, = struct.unpack("!H", pkt[:2])
        self.assertEqual(opcode, OP_WRQ)

    def test_filename_in_packet(self):
        pkt = build_wrq("relatorio.pdf")
        self.assertIn(b"relatorio.pdf\x00", pkt)

    def test_default_mode_is_octet(self):
        pkt = build_wrq("file.txt")
        self.assertIn(b"octet\x00", pkt)

    def test_empty_filename_raises(self):
        with self.assertRaises(ValueError):
            build_wrq("")


class TestBuildData(unittest.TestCase):

    def test_opcode_is_data(self):
        pkt = build_data(1, b"hello")
        opcode, = struct.unpack("!H", pkt[:2])
        self.assertEqual(opcode, OP_DATA)

    def test_block_number_encoded(self):
        pkt = build_data(7, b"abc")
        _, block = struct.unpack("!HH", pkt[:4])
        self.assertEqual(block, 7)

    def test_data_payload_appended(self):
        payload = b"hello world"
        pkt = build_data(1, payload)
        self.assertEqual(pkt[4:], payload)

    def test_total_length(self):
        payload = b"hello"
        pkt = build_data(1, payload)
        self.assertEqual(len(pkt), 4 + len(payload))

    def test_full_block(self):
        payload = b"x" * BLOCK_SIZE
        pkt = build_data(1, payload)
        self.assertEqual(len(pkt), 4 + BLOCK_SIZE)

    def test_empty_data_allowed(self):
        pkt = build_data(1, b"")
        self.assertEqual(len(pkt), 4)

    def test_data_exceeds_block_size_raises(self):
        with self.assertRaises(ValueError):
            build_data(1, b"x" * (BLOCK_SIZE + 1))

    def test_block_zero_raises(self):
        with self.assertRaises(ValueError):
            build_data(0, b"data")

    def test_block_above_max_raises(self):
        with self.assertRaises(ValueError):
            build_data(65536, b"data")

    def test_max_block_number_allowed(self):
        pkt = build_data(65535, b"x")
        _, block = struct.unpack("!HH", pkt[:4])
        self.assertEqual(block, 65535)


class TestBuildAck(unittest.TestCase):

    def test_opcode_is_ack(self):
        pkt = build_ack(1)
        opcode, = struct.unpack("!H", pkt[:2])
        self.assertEqual(opcode, OP_ACK)

    def test_block_number_encoded(self):
        pkt = build_ack(42)
        _, block = struct.unpack("!HH", pkt[:4])
        self.assertEqual(block, 42)

    def test_ack_zero_for_wrq(self):
        pkt = build_ack(0)
        _, block = struct.unpack("!HH", pkt[:4])
        self.assertEqual(block, 0)

    def test_length_always_four(self):
        for n in (0, 1, 255, 65535):
            self.assertEqual(len(build_ack(n)), 4)

    def test_negative_block_raises(self):
        with self.assertRaises(ValueError):
            build_ack(-1)

    def test_block_above_max_raises(self):
        with self.assertRaises(ValueError):
            build_ack(65536)


class TestBuildError(unittest.TestCase):

    def test_opcode_is_error(self):
        pkt = build_error(1)
        opcode, = struct.unpack("!H", pkt[:2])
        self.assertEqual(opcode, OP_ERROR)

    def test_error_code_encoded(self):
        pkt = build_error(2)
        _, code = struct.unpack("!HH", pkt[:4])
        self.assertEqual(code, 2)

    def test_default_message_used(self):
        pkt = build_error(1)
        self.assertIn(b"File not found", pkt)

    def test_custom_message_used(self):
        pkt = build_error(0, "custom error")
        self.assertIn(b"custom error", pkt)

    def test_message_null_terminated(self):
        pkt = build_error(1)
        self.assertTrue(pkt.endswith(b"\x00"))

    def test_invalid_error_code_raises(self):
        with self.assertRaises(ValueError):
            build_error(8)

    def test_negative_error_code_raises(self):
        with self.assertRaises(ValueError):
            build_error(-1)

    def test_all_standard_codes_build(self):
        for code in range(8):
            pkt = build_error(code)
            self.assertGreater(len(pkt), 4)


if __name__ == "__main__":
    unittest.main()
