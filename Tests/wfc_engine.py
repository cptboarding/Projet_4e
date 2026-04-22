
from dataclasses import dataclass


@dataclass
class Compatibility:
    up: tuple[int, ...]
    down: tuple[int, ...]
    right: tuple[int, ...]
    left: tuple[int, ...]


class TileBlueprint:

    def __init__(self, value: int, x: int, y: int):
        self.value = value
        self.x = x
        self.y =  y
        self.comp: Compatibility = Compatibility((), (), (), ())

    def set_compatibility(self, **kwargs):
        for i in kwargs:
            setattr(self.comp, i, kwargs[i])

class TileEmpty(TileBlueprint):

    def __post_init__(self):
        max_tiles = 14
        full = tuple([i for i in range(max_tiles)])
        self.comp = Compatibility(full, full, full, full)

    def check_surrounding_comp(self,
                               right: TileBlueprint | "TileEmpty",
                               left: TileBlueprint | "TileEmpty",
                               up: TileBlueprint | "TileEmpty",
                               down: TileBlueprint | "TileEmpty"
                               ):
        pass



if __name__ == "__main__":
    t = TileBlueprint(1, 0, 0)
    print(t.comp)