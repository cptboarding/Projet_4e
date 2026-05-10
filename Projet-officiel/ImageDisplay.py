
"""
Placeholder object for any image
Places said image into a sprite
"""


import pyglet
from pyglet.gl import *

from typing import Literal
from typing import TYPE_CHECKING
"""
Since Camera is in another file and it's a bother to import the whole thing solely for the typing convention, what you 
can do is only import what you need at the time you need, not create loops of imports during runtime (you might crash 
your computer otherwise)
"""
if TYPE_CHECKING:
    from Camera import Camera


class ImageDisplay:

    def __init__(self,
                 camera: "Camera",
                 batch: Literal["UI", "game"],
                 layer: int = 0,
                 position: tuple[int, int] = (0, 0),
                 centered: bool = True,
                 size: float = 1.0):

        self.camera = camera
        self.layer = layer
        #if needed to hide at some point
        self.visible = True

        self.pos_x = position[0]
        self.pos_y = position[1]

        self.centered = centered
        self.size = size

        #placeholder
        self.texture = pyglet.image.SolidColorImagePattern(color=(255, 0, 0, 255)).create_image(32, 32)

        if batch == "game":
            self.batch = camera.batch_game
        elif batch == "UI":
            self.batch = camera.batch_UI

        self.sprite: pyglet.sprite.Sprite = pyglet.sprite.Sprite(self.texture, batch=self.batch)
        self.camera.add_to_layer(self.sprite, self.layer)


    #image handling -------------------------------------------------------------------------

    #add/overwrite with already known source
    def add_image(self, texture):
        self.sprite.image = texture

    #search and load
    def import_image(self, name: str, path: str = "."):
        try:
            pyglet.resource.path = [path]
            pyglet.resource.reindex()

            img = pyglet.image.load(name)
        except:
            print("Image not found")
        else:
            self.sprite.image = img


    #sprite stuff ---------------------------------------------------------------------

    def set_sprite_nearest(self):
        texture = self.sprite.image.get_texture()

        glBindTexture(texture.target, texture.id)
        glTexParameteri(texture.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    @property
    def texture_dim(self) -> list[int]:
        texture = self.sprite.image.get_texture()
        return [texture.width, texture.height]

    @property
    def texture_dim_scaled(self):
        return self.texture_dim[0] * self.scale, self.texture_dim[1] * self.scale

    @property
    def texture_offset(self) -> list[int]:
        return [int(self.texture_dim_scaled[0] // 2), int(self.texture_dim_scaled[0] // 2)]

    @property
    def texture_dim_static(self):
        return self.texture_dim[0] * self.size, self.texture_dim[1] * self.size

    @property
    def texture_offset_static(self) -> list[int]:
        return [int(self.texture_dim_static[0] // 2), int(self.texture_dim_static[0] // 2)]

    @property
    def downside_corner(self) -> list[int]:
        return [self.pos_x - self.texture_offset_static[0], self.pos_y - self.texture_offset_static[1]]

    @property
    def viewport_pos(self):
        return self.camera.get_position_on_viewport(self.pos_x, self.pos_y)

    @property
    def viewport_pos_downside(self):
        return self.camera.get_position_on_viewport(self.downside_corner[0], self.downside_corner[1])

    @property
    def scale(self):
        return self.sprite.scale

    #for centering
    def sprite_pos_offset(self):
        self.sprite.x -= self.texture_offset[0]
        self.sprite.y -= self.texture_offset[1]

    #reposition according to camera, update zoom
    #if no camera, stay in position
    def update_sprite_pos(self):
        if self.camera is not None:
            self.sprite.scale = self.camera.zoom_scale * self.size
            vp = self.viewport_pos
            self.sprite.x = vp[0]
            self.sprite.y = vp[1]

        #no camera handling
        else:
            self.sprite.x = self.pos_x
            self.sprite.y = self.pos_y

        #always center
        if self.centered:
            self.sprite_pos_offset()

    #runtime update
    def update(self):
        self.set_sprite_nearest()
        self.update_sprite_pos()