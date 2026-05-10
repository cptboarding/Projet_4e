

from typing import TYPE_CHECKING
#same story as ImageDisplay.py
if TYPE_CHECKING:
    from Camera import Camera

import math


class CollisionShape:

    def __init__(self, position: tuple[int, int], shape: str):
        self.position = position
        self.shape = shape



class CircleShape(CollisionShape):
    def __init__(self,
                 position: tuple[int, int],
                 shape: str,
                 radius: float = 100):
        super().__init__(position, shape="circle")
        self.radius = radius

    @property
    def radius_2(self) -> float:
        return self.radius ** 2

    @staticmethod
    def euclidean_distance(x1, y1, x2, y2) -> float:
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    @staticmethod
    def euclidean_distance_2(x1, y1, x2, y2) -> float:
        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def is_point_colliding(self, point: tuple[int, int]):
        d2 = self.euclidean_distance_2(self.position[0], self.position[1], point[0], point[1])
        if d2 <= self.radius_2:




