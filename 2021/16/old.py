import sys

def read_bit(data, num):
    base = int(num // 8)
    shift = int((num * -1 + 7) % 8)
    return (data[base] >> shift) & 0b1

def read_bits(data, start, num):
    bits = 0
    for i in range(num):
        bits = bits << 1
        bits += read_bit(data, start + i)
    return bits

class Packet:
    def __init__(self, data, cur):
        self.version = read_bits(data, cur, 3)
        self.type_id = read_bits(data, cur + 3, 3)

        if self.type_id == 4:
            self.literal_packet(data, cur + 6)

    def literal_packet(self, data, cur):
        self.value = 0
        while True:
            cont = read_bits(data, cur, 1)
            self.value = (self.value << 4) + read_bits(data, cur + 1, 4)
            cur += 5
            if cont == 0:
                return

def literal_packet(packet, start):
    value = 0
    while True:
        cont = read_bits(packet, start, 1)
        value = (value << 4) + read_bits(packet, start + 1, 4)
        start += 5
        if cont == 0:
            return (start, value)

def read_operands(packet, start):
    len_type = read_bits(packet, start, 1)
    operands = []
    if len_type == 0:
        length = start + 1 + read_bits(packet, start + 1, 15)
        cur = start + 1 + 15

        while cur < length:
            ln, val = process_packet(packet, cur)
            cur = ln
            operands.append(val)
    else:
        packets = read_bits(packet, start + 1, 11)
        cur = start + 1 + 11

        for i in range(packets):
            ln, val = process_packet(packet, cur)
            cur = ln
            operands.append(val)

    return operands


def process_packet(packet, start):
    #print([read_bit(packet, x) for x in range(len(packet)*8)])

    # read header, version and type
    version = read_bits(packet, start, 3)
    versions += version
    type_id = read_bits(packet, start + 3, 3)

    if type_id == 4:
        return literal_packet(packet, start + 6)
    else:
        operands = read_operands(packet, start + 6)
        print(read_operands(packet, start + 6))


for line in sys.stdin:
    packet = bytes.fromhex(line.strip())

    print(process_packet(packet, 0))
    print(versions)
