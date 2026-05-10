

"""
encoder/decoder
bytes --> text
"""


from dataclasses import dataclass
from typing import Literal


format = 'RGBA'
format_len = len(format)

@dataclass
class Converter:
    data: tuple[list[str, bytes], ...] = (
        ["W", b'/x00/x00/x00/x00'],
        ["G", b'/x00/x00/x00/x00'],
        ["C", b'/x00/x00/x00/x00'],
        ["V", b'/x00/x00/x00/x00'],
    )

    def conversion(self, arg: str | bytes) -> str | bytes:
        def check():
            for i in range(len(self.data)):
                if arg in self.data[i]:
                    print(i)
                    return i
            print("404 not found")
            return False

        c = check()
        if isinstance(c, int):
            p = (self.data[c].index(arg) + 1) % 2
            return self.data[c][p]
        else:
            return ""

if __name__ == "__main__":
    c = Converter()
    print(c.conversion("W"))
