

"""
encoder/decoder
bytes --> text
"""


from dataclasses import dataclass

format = 'RGBA'
format_len = len(format)

@dataclass
class Encoder:

    data = {
        "WATER": b'\x00\x00\xff\xff',
        "GROUND": b'\x00\xff\x00\xff',
        "MOUNTAIN": b'\xff\x00\x00\xff',
        "EMPTY": b'\x00\x00\x00\xff',
    }

    def full_encode(self, arg):
        encoding = ""
        i = 0
        r = bytearray()
        while i != len(arg):
            if arg[i] == '/':
                r.extend(self.data[encoding])
                encoding = ""
            else:
                encoding += arg[i]
            i += 1
        return r

@dataclass
class Decoder:

    @staticmethod
    def get_packet(data, index, size=format_len):
        start = index * size
        return data[start:start + size]

    @staticmethod
    def decode(arg):
        if arg == b'\x00\x00\xff\xff':
            return 'WATER'
        elif arg == b'\x00\xff\x00\xff':
            return 'GROUND'
        elif arg == b'\xff\x00\x00\xff':
            return 'MOUNTAIN'
        elif arg == b'\x00\x00\x00\xff':
            return 'EMPTY'

    def full_decode(self, arg: bytearray):
        r = ""
        for i in range(int(len(arg)/format_len)):
            b = self.get_packet(arg, i)
            r += self.decode(b) + '/'
        return r
