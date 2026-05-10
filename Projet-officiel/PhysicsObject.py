

from ImageDisplay import ImageDisplay

from typing import Literal
from typing import TYPE_CHECKING
#same story as ImageDisplay.py
if TYPE_CHECKING:
    from Camera import Camera

class PhysicsObject(ImageDisplay):

    def __init__(self,
                 camera: "Camera",
                 batch: Literal["UI", "game"],
                 layer: int = 0,

                 position: tuple[int, int] = (0, 0),
                 centered: bool = True,
                 size: float = 1.0,
                 ):
        super().__init__(camera, batch, layer, position, centered, size)
        self.shape = None

