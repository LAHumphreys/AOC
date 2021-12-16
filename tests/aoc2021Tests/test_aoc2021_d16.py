from unittest import TestCase
from typing import List

from aoc2021.d16 import expand, bin_to_dex, parse_packet_type, get_literal_data, load_from_file
from aoc2021.d16 import Packet, PacketType, read_packets, get_operator_length, LengthType, check_sum
from aoc2021.d16 import get_value
from tests.aoc2021Tests.aoc2021_common import get_test_file_path

class Parser(TestCase):
    def test_parser(self):
        self.assertEqual(expand("D2FE28"), "110100101111111000101000")
        self.assertEqual(expand("38006F45291200"), "00111000000000000110111101000101001010010001001000000000")
        self.assertEqual(expand("EE00D40C823060"), "11101110000000001101010000001100100000100011000001100000")

    def test_bin_parser(self):
        self.assertEqual(bin_to_dex("110"), 6)
        self.assertEqual(bin_to_dex("100"), 4)
        self.assertEqual(bin_to_dex("011111100101"), 2021)

    def test_packet_type(self):
        self.assertEqual(parse_packet_type("110100101111111000101000"), PacketType.LITERAL)
        self.assertNotEqual(parse_packet_type("00111000000000000110111101000101001010010001001000000000"), PacketType.LITERAL)
        self.assertNotEqual(parse_packet_type("11101110000000001101010000001100100000100011000001100000"), PacketType.LITERAL)

    def test_single_literal_packet(self):
        packets = read_packets("110100101111111000101000")
        self.assertEqual(len(packets), 1)
        packet = packets[0]
        self.assertEqual(packet.packet_type, PacketType.LITERAL)
        self.assertEqual(packet.packet_version, 6)
        self.assertEqual(packet.data, "011111100101")
        self.assertEqual(packet.packets, [])

    def test_operator_length(self):
        length_type, length = get_operator_length("00000000000110111101000101001010010001001000000000")
        self.assertEqual(length_type, LengthType.LENGTH)
        self.assertEqual(length, 27)

    def test_operator_length_count(self):
        length_type, length = get_operator_length("1000000000110101000000110010000010001100000110000")
        self.assertEqual(length_type, LengthType.COUNT)
        self.assertEqual(length, 3)

    def test_multiple_packets(self):
        packets: List[Packet] = read_packets("110100010100101001000100100")
        self.assertEqual(len(packets), 2)
        first, second = packets
        self.assertEqual(first.packet_type, PacketType.LITERAL)
        self.assertEqual(bin_to_dex(first.data), 10)
        self.assertEqual(second.packet_type, PacketType.LITERAL)
        self.assertEqual(bin_to_dex(second.data), 20)

    def test_multiple_packets_length_bound(self):
        packets: List[Packet] = read_packets("110100010100101001000100100110100010100101001000100100", max_length=27)
        self.assertEqual(len(packets), 2)
        first, second = packets
        self.assertEqual(first.packet_type, PacketType.LITERAL)
        self.assertEqual(bin_to_dex(first.data), 10)
        self.assertEqual(second.packet_type, PacketType.LITERAL)
        self.assertEqual(bin_to_dex(second.data), 20)

    def test_multiple_packets_count_bound(self):
        packets: List[Packet] = read_packets("110100010100101001000100100110100010100101001000100100", max_count=3)
        self.assertEqual(len(packets), 3)
        first, second, third = packets
        self.assertEqual(first.packet_type, PacketType.LITERAL)
        self.assertEqual(bin_to_dex(first.data), 10)
        self.assertEqual(second.packet_type, PacketType.LITERAL)
        self.assertEqual(bin_to_dex(second.data), 20)
        self.assertEqual(third.packet_type, PacketType.LITERAL)
        self.assertEqual(bin_to_dex(third.data), 10)

    def test_length_operator(self):
        packets = read_packets("00111000000000000110111101000101001010010001001000000000")
        self.assertEqual(len(packets), 1)
        packet = packets[0]
        self.assertNotEqual(packet.packet_type, PacketType.LITERAL)
        self.assertEqual(packet.packet_version, 1)
        self.assertEqual(len(packet.packets), 2)

    def test_count_operator(self):
        packets = read_packets("11101110000000001101010000001100100000100011000001100000")
        self.assertEqual(len(packets), 1)
        packet = packets[0]
        self.assertNotEqual(packet.packet_type, PacketType.LITERAL)
        self.assertEqual(packet.packet_version, 7)
        self.assertEqual(len(packet.packets), 3)
        sub_packets: List[Packet] = [sub for sub in packet.packets]
        self.assertEqual(sub_packets[0].packet_type, PacketType.LITERAL)
        self.assertEqual(bin_to_dex(sub_packets[0].data), 1)
        self.assertEqual(sub_packets[1].packet_type, PacketType.LITERAL)
        self.assertEqual(bin_to_dex(sub_packets[1].data), 2)
        self.assertEqual(sub_packets[2].packet_type, PacketType.LITERAL)
        self.assertEqual(bin_to_dex(sub_packets[2].data), 3)

    def test_literal_data(self):
        self.assertEqual(get_literal_data("101111111000101000"), ("011111100101", "000"))

    def test_sample_one(self):
        bin_code = expand("8A004A801A8002F478")
        packets = read_packets(bin_code)
        self.assertEqual(len(packets), 1)
        self.assertNotEqual(packets[0].packet_type, PacketType.LITERAL)
        self.assertEqual(packets[0].packet_version, 4)
        self.assertEqual(len(packets[0].packets), 1)
        self.assertNotEqual(packets[0].packets[0].packet_type, PacketType.LITERAL)
        self.assertEqual(packets[0].packets[0].packet_version, 1)
        self.assertEqual(len(packets[0].packets[0].packets), 1)
        self.assertNotEqual(packets[0].packets[0].packets[0].packet_type, PacketType.LITERAL)
        self.assertEqual(packets[0].packets[0].packets[0].packet_version, 5)
        self.assertEqual(packets[0].packets[0].packets[0].packets[0].packet_type, PacketType.LITERAL)
        self.assertEqual(packets[0].packets[0].packets[0].packets[0].packet_version, 6)

        self.assertEqual(check_sum(packets[0]), 16)

    def test_sample_two(self):
        bin_code = expand("620080001611562C8802118E34")
        packets = read_packets(bin_code)
        self.assertEqual(len(packets), 1)
        self.assertEqual(check_sum(packets[0]), 12)

    def test_sample_three(self):
        bin_code = expand("C0015000016115A2E0802F182340")
        packets = read_packets(bin_code)
        self.assertEqual(len(packets), 1)
        self.assertEqual(check_sum(packets[0]), 23)

    def test_sample_file(self):
        bin_code = load_from_file(get_test_file_path("samples/d16.txt"))
        packets = read_packets(bin_code)
        self.assertEqual(len(packets), 1)
        self.assertEqual(check_sum(packets[0]), 31)


class Values(TestCase):
    def test_literal(self):
        bin_code = expand("D2FE28")
        packets = read_packets(bin_code)
        self.assertEqual(len(packets), 1)
        self.assertEqual(get_value(packets[0]), 2021)

    def test_sum(self):
        bin_code = expand("C200B40A82")
        packets = read_packets(bin_code)
        self.assertEqual(len(packets), 1)
        self.assertEqual(get_value(packets[0]), 3)

    def test_product(self):
        bin_code = expand("04005AC33890")
        packets = read_packets(bin_code)
        self.assertEqual(len(packets), 1)
        self.assertEqual(get_value(packets[0]), 54)

    def test_minimum(self):
        bin_code = expand("880086C3E88112")
        packets = read_packets(bin_code)
        self.assertEqual(len(packets), 1)
        self.assertEqual(get_value(packets[0]), 7)

    def test_maximum(self):
        bin_code = expand("CE00C43D881120")
        packets = read_packets(bin_code)
        self.assertEqual(len(packets), 1)
        self.assertEqual(get_value(packets[0]), 9)

    def test_less_than(self):
        bin_code = expand("D8005AC2A8F0")
        packets = read_packets(bin_code)
        self.assertEqual(len(packets), 1)
        self.assertEqual(get_value(packets[0]), 1)

    def test_greater_than(self):
        bin_code = expand("F600BC2D8F")
        packets = read_packets(bin_code)
        self.assertEqual(len(packets), 1)
        self.assertEqual(get_value(packets[0]), 0)

    def test_equal(self):
        bin_code = expand("9C005AC2F8F0")
        packets = read_packets(bin_code)
        self.assertEqual(len(packets), 1)
        self.assertEqual(get_value(packets[0]), 0)

    def test_example(self):
        bin_code = expand("9C0141080250320F1802104A08")
        packets = read_packets(bin_code)
        self.assertEqual(len(packets), 1)
        self.assertEqual(get_value(packets[0]), 1)
