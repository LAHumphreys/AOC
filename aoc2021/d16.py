from typing import Tuple, List
from dataclasses import dataclass
from enum import Enum


class Unhandled(Exception):
    pass


def load_from_file(path: str) -> str:
    with open(path, encoding="ascii") as file:
        lines = [line.replace("\n", "") for line in file.readlines()]

    if len(lines) != 1:
        raise Unhandled

    return expand(lines[0])


def expand(hex_str: str) -> str:
    result = ""
    for hex_digit in hex_str:
        result += f"{int(hex_digit, 16):04b}"
    return result


def bin_to_dex(bin_str: str) -> int:
    return int(bin_str, 2)


class PacketType(Enum):
    LITERAL = 4
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    GREATER_THAN = 5
    LESS_THAN = 6
    EQUAL = 7
    OPERATOR = -1


@dataclass
class Packet:
    packet_type: PacketType
    packet_version: int
    data: str
    packets: []


def parse_packet_type(packet: str) -> PacketType:
    packet_type = bin_to_dex(packet[3:6])
    return PacketType(packet_type)


def get_value(packet: Packet) -> int:
    if packet.packet_type == PacketType.LITERAL:
        value = bin_to_dex(packet.data)
    elif packet.packet_type == PacketType.SUM:
        value = 0
        for sub_packet in packet.packets:
            value += get_value(sub_packet)
    elif packet.packet_type == PacketType.PRODUCT:
        value = 1
        for sub_packet in packet.packets:
            value *= get_value(sub_packet)
    elif packet.packet_type == PacketType.MINIMUM:
        value = min(get_value(sub_packet) for sub_packet in packet.packets)
    elif packet.packet_type == PacketType.MAXIMUM:
        value = max(get_value(sub_packet) for sub_packet in packet.packets)
    elif packet.packet_type == PacketType.LESS_THAN:
        value = get_value(packet.packets[0]) < get_value(packet.packets[1])
    elif packet.packet_type == PacketType.GREATER_THAN:
        value = get_value(packet.packets[0]) > get_value(packet.packets[1])
    elif packet.packet_type == PacketType.EQUAL:
        value = get_value(packet.packets[0]) == get_value(packet.packets[1])
    else:
        raise Unhandled

    return value


def _read_packets(bin_str: str,
                  max_length: int = None,
                  max_count: int = None) -> Tuple[List[Packet], str, str]:
    if not max_length:
        min_length = 7
    else:
        min_length = len(bin_str) - max_length

    if not max_count:
        max_count = len(bin_str)

    packets = []
    read_data = ""
    while len(bin_str) > min_length and len(packets) < max_count:
        packet_type = parse_packet_type(bin_str)
        packet_version = bin_to_dex(bin_str[0:3])
        if packet_type == PacketType.LITERAL:
            read_data += bin_str[0:6]
            data, bin_str = get_literal_data(bin_str[6:])
            read_data += data
            sub_packets = []
        else:
            length_type, length = get_operator_length(bin_str[6:])
            if length_type == LengthType.LENGTH:
                read_data += bin_str[:22]
                sub_packets, bin_str, data = _read_packets(bin_str[22:], max_length=length)
            elif length_type == LengthType.COUNT:
                read_data += bin_str[:18]
                sub_packets, bin_str, data = _read_packets(bin_str[18:], max_count=length)
            else:
                raise Unhandled

        packets.append(Packet(
            packet_version=packet_version,
            packet_type=packet_type,
            data=data,
            packets=sub_packets
        ))
    return packets, bin_str, read_data


def read_packets(bin_str: str, max_length: int = None, max_count: int = None) -> List[Packet]:
    return _read_packets(bin_str, max_length, max_count)[0]


def get_literal_data(bin_data: str) -> Tuple[str, str]:
    result = ""
    index = 0
    while bin_data[index] == "1":
        index += 1
        result += bin_data[index:index+4]
        index += 4
    index += 1
    result += bin_data[index+0:index+4]
    index += 4

    return result, bin_data[index:]


class LengthType(Enum):
    COUNT = 1
    LENGTH = 0


def get_operator_length(bin_data: str) -> Tuple[LengthType, int]:
    if bin_data[0] == "0":
        length_type = LengthType.LENGTH
        length = bin_to_dex(bin_data[1:16])
    else:
        length_type = LengthType.COUNT
        length = bin_to_dex(bin_data[1:12])

    return length_type, length


def check_sum(packet: Packet) -> int:
    total = packet.packet_version
    if packet.packets:
        for sub_packet in packet.packets:
            total += check_sum(sub_packet)
    return total


if __name__ == "__main__":
    def main():
        raw_message = load_from_file("input/d16.txt")
        packets = read_packets(raw_message)
        if len(packets) != 1:
            raise Unhandled
        print(check_sum(packets[0]))
        print(get_value(packets[0]))
    main()
