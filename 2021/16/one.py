import sys
import math

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
            self.end = self.read_literal(data, cur + 6)
        else:
            self.end = self.read_operands(data, cur + 6)

    def read_literal(self, data, cur):
        self.value = 0
        while True:
            cont = read_bits(data, cur, 1)
            self.value = (self.value << 4) + read_bits(data, cur + 1, 4)
            cur += 5
            if cont == 0:
                return cur

    def read_operands(self, data, cur):
        len_type = read_bits(data, cur, 1)
        self.operands = []
        if len_type == 0:
            length = cur + 1 + 15 + read_bits(data, cur + 1, 15)
            cur = cur + 1 + 15

            while cur < length:
                p = Packet(data, cur)
                cur = p.end
                self.operands.append(p)
        else:
            num_packets = read_bits(data, cur + 1, 11)
            cur = cur + 1 + 11

            for i in range(num_packets):
                p = Packet(data, cur)
                cur = p.end
                self.operands.append(p)
        return cur

    def versions(self):
        if self.type_id == 4:
            return self.version

        versions = self.version
        for p in self.operands:
            versions += p.versions()
        return versions

    def calculate(self):
        if self.type_id == 4:
            return self.value

        op_vals = [p.calculate() for p in self.operands]

        if self.type_id == 0:
            return sum(op_vals)
        if self.type_id == 1:
            return math.prod(op_vals)
        if self.type_id == 2:
            return min(op_vals)
        if self.type_id == 3:
            return max(op_vals)
        if self.type_id == 5:
            if op_vals[0] > op_vals[1]:
                return 1
            return 0
        if self.type_id == 6:
            if op_vals[0] < op_vals[1]:
                return 1
            return 0
        if self.type_id == 7:
            if op_vals[0] == op_vals[1]:
                return 1
            return 0





for line in sys.stdin:
    data = bytes.fromhex(line.strip())

    packet = Packet(data, 0)

    print(packet.versions())
    print(packet.calculate())
    print()
