"""
tests/test_parsers.py - Testes unitários para packets/tftp_parsers.py

Cobre a interpretação correta de cada tipo de pacote TFTP e a detecção
de pacotes malformados.
"""

import struct
import unittest

from packets.tftp_packets import (
    parse_packet,
    OP_ACK,
    OP_DATA,
    OP_ERROR,
    OP_RRQ,
    OP_WRQ,
)


class TestParseRrq(unittest.TestCase):

    def _make_rrq(self, filename, mode="octet"):
        return (
            struct.pack("!H", OP_RRQ)
            + filename.encode("ascii") + b"\x00"
            + mode.encode("ascii") + b"\x00"
        )

    def test_opcode_returned(self):
        result = parse_packet(self._make_rrq("file.txt"))
        self.assertEqual(result["opcode"], OP_RRQ)

    def test_filename_returned(self):
        result = parse_packet(self._make_rrq("foto.png"))
        self.assertEqual(result["filename"], "foto.png")

    def test_mode_returned(self):
        result = parse_packet(self._make_rrq("file.txt", "netascii"))
        self.assertEqual(result["mode"], "netascii")

    def test_missing_null_terminator_raises(self):
        bad = struct.pack("!H", OP_RRQ) + b"file.txt"
        with self.assertRaises(ValueError):
            parse_packet(bad)


class TestParseWrq(unittest.TestCase):

    def _make_wrq(self, filename, mode="octet"):
        return (
            struct.pack("!H", OP_WRQ)
            + filename.encode("ascii") + b"\x00"
            + mode.encode("ascii") + b"\x00"
        )

    def test_opcode_returned(self):
        result = parse_packet(self._make_wrq("upload.bin"))
        self.assertEqual(result["opcode"], OP_WRQ)

    def test_filename_returned(self):
        result = parse_packet(self._make_wrq("upload.bin"))
        self.assertEqual(result["filename"], "upload.bin")

    def test_mode_returned(self):
        result = parse_packet(self._make_wrq("upload.bin"))
        self.assertEqual(result["mode"], "octet")


class TestParseData(unittest.TestCase):

    def _make_data(self, block, payload):
        return struct.pack("!HH", OP_DATA, block) + payload

    def test_opcode_returned(self):
        result = parse_packet(self._make_data(1, b"hello"))
        self.assertEqual(result["opcode"], OP_DATA)

    def test_block_number_returned(self):
        result = parse_packet(self._make_data(5, b"abc"))
        self.assertEqual(result["block_number"], 5)

    def test_data_payload_returned(self):
        payload = b"test data"
        result = parse_packet(self._make_data(1, payload))
        self.assertEqual(result["data"], payload)

    def test_empty_data_allowed(self):
        result = parse_packet(self._make_data(1, b""))
        self.assertEqual(result["data"], b"")

    def test_too_short_raises(self):
        with self.assertRaises(ValueError):
            parse_packet(struct.pack("!H", OP_DATA) + b"\x01")


class TestParseAck(unittest.TestCase):

    def _make_ack(self, block):
        return struct.pack("!HH", OP_ACK, block)

    def test_opcode_returned(self):
        result = parse_packet(self._make_ack(3))
        self.assertEqual(result["opcode"], OP_ACK)

    def test_block_number_returned(self):
        result = parse_packet(self._make_ack(42))
        self.assertEqual(result["block_number"], 42)

    def test_ack_zero_returned(self):
        result = parse_packet(self._make_ack(0))
        self.assertEqual(result["block_number"], 0)

    def test_too_short_raises(self):
        with self.assertRaises(ValueError):
            parse_packet(struct.pack("!H", OP_ACK) + b"\x00")


class TestParseError(unittest.TestCase):

    def _make_error(self, code, msg=""):
        return (
            struct.pack("!HH", OP_ERROR, code)
            + msg.encode("ascii") + b"\x00"
        )

    def test_opcode_returned(self):
        result = parse_packet(self._make_error(1, "not found"))
        self.assertEqual(result["opcode"], OP_ERROR)

    def test_error_code_returned(self):
        result = parse_packet(self._make_error(2, "access violation"))
        self.assertEqual(result["error_code"], 2)

    def test_error_msg_returned(self):
        result = parse_packet(self._make_error(1, "File not found"))
        self.assertEqual(result["error_msg"], "File not found")

    def test_empty_message_allowed(self):
        result = parse_packet(self._make_error(0, ""))
        self.assertEqual(result["error_msg"], "")

    def test_too_short_raises(self):
        with self.assertRaises(ValueError):
            parse_packet(struct.pack("!HH", OP_ERROR, 1))


class TestParseEdgeCases(unittest.TestCase):

    def test_too_short_raises(self):
        with self.assertRaises(ValueError):
            parse_packet(b"\x00")

    def test_empty_bytes_raises(self):
        with self.assertRaises(ValueError):
            parse_packet(b"")

    def test_unknown_opcode_raises(self):
        with self.assertRaises(ValueError):
            parse_packet(struct.pack("!H", 99))


if __name__ == "__main__":
    unittest.main()
