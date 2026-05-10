
"""
The ultimate GOATesque map
MxN pixels inside an image with removed snap to create a fast tiled map

"""

import random
import pyglet
from ImageDisplay import ImageDisplay

from typing import Literal
from typing import TYPE_CHECKING

#same story as ImageDisplay.py
if TYPE_CHECKING:
    from Camera import Camera


#inherits image displayer
class SquareMap(ImageDisplay):

    def __init__(self,
                 camera: "Camera",
                 batch: Literal["UI", "game"],
                 layer: int = 0,

                 #define parameters for the map itself
                 map_dimensions: tuple[int, int] = (0, 0),
                 map_pixel_size: int = 4,
                 map_pixel_format: str = "RGBA",

                 #better to have some factory settings for simplicity, still flexible
                 position: tuple[int, int] = (0, 0),
                 centered: bool = True,
                 size: float = 1.0):

        """
        Variable creation:
        Variables --> camera // visible // pos_x, pos_y // centered // size
        Pyglet window --> texture // sprite
        """
        super().__init__(camera, batch, layer, position, centered, size)

        self.dim_x = map_dimensions[0]
        self.dim_y = map_dimensions[1]

        self.pixel_size = map_pixel_size
        self.pixel_format = map_pixel_format

        #set image data
        self.pixel_array: bytearray = bytearray(self.dim_x * self.dim_y * len(self.pixel_format))
        self.pitch = self.dim_x * len(self.pixel_format) #pitch meaning the length of a line of the bytearray

        self.image_data: pyglet.image.ImageData = pyglet.image.ImageData(
            self.dim_x,
            self.dim_y,
            self.pixel_format,
            bytes(self.pixel_array),
            pitch=self.pitch
        )

    #image handling --------------------------------------------------------------------

    #update the data because you also need to update the objects' values, also resets the whole thing
    #not to overuse on runtime because object creation and deletion is costly
    def update_data_values(self,
                           map_dimensions: tuple[int, int],
                           map_pixel_size: int,
                           map_pixel_format: str = "RGBA",
                           ):
        self.dim_x = map_dimensions[0]
        self.dim_y = map_dimensions[1]
        self.pixel_size = map_pixel_size
        self.pixel_format = map_pixel_format
        self.pixel_array: bytearray = bytearray(self.dim_x * self.dim_y * len(self.pixel_format))
        self.pitch = self.dim_x * len(self.pixel_format)
        self.image_data: pyglet.image.ImageData = pyglet.image.ImageData(
            self.dim_x,
            self.dim_y,
            self.pixel_format,
            bytes(self.pixel_array),
            pitch=self.pitch
        )

    #update ImageData object with values + update sprite
    def update_image(self):
        self.image_data.set_data(self.pixel_format, self.pitch, bytes(self.pixel_array))
        self.sprite.image = self.image_data

    @property
    def tile_size(self):
        d = self.texture_dim_scaled
        return max(d[0] / self.dim_x, d[1] / self.dim_y)

    #replace byte at position (x, y)
    def set_pixel(self, pos: tuple[int, int], rgb: tuple[int, int, int], a: int = 255):
        x = pos[0]
        y = pos[1]
        i = (y*self.dim_x + x) * 4

        self.pixel_array[i] = rgb[0]
        self.pixel_array[i+1] = rgb[1]
        self.pixel_array[i+2] = rgb[2]
        self.pixel_array[i+3] = a

    #random test for debug and a cool QR code
    def rand_test(self):
        for y in range(self.dim_y):
            for x in range(self.dim_x):
                self.set_pixel((x, y), (255*random.randint(0, 1), 0, 0))

    #runtime ---------------------------------------------------------------------------

    #insert the image and forward to image display
    def update(self):
        self.update_image()
        super().update()
