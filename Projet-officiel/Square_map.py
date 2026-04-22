import pyglet
import random
from pyglet.gl import *


class Square:

    def __init__(self, viewport=None, x_dim=500, y_dim=500):

        self.camera = viewport
        self.pos_x = 0
        self.pos_y = 0
        self.centered = True
        self.visible = True

        self.dim_x = x_dim
        self.dim_y = x_dim

        self.format = 'RGBA'
        self.pixels = bytearray(self.dim_x * self.dim_y * len(self.format))
        self.pitch = self.dim_x * len(self.format)

        self.image_data = pyglet.image.ImageData(
            self.dim_x,
            self.dim_y,
            self.format,
            bytes(self.pixels),
            pitch=self.pitch
        )

        self.texture = pyglet.image.Texture.create(self.dim_x, self.dim_y)
        self.texture.blit_into(self.image_data, 0, 0, 0)

        self.sprite = pyglet.sprite.Sprite(self.texture)



    def rand_test(self):
        for y in range(self.dim_y):
            for x in range(self.dim_x):
                self.set_pixel((x, y), (255*random.randint(0, 1), 0, 0))

    def set_pixel(self, pos: tuple[int, int], rgb: tuple[int, int, int], a: int = 255):
        x = pos[0]
        y = pos[1]
        i = (y*self.dim_x + x) * 4

        self.pixels[i] = rgb[0]
        self.pixels[i+1] = rgb[1]
        self.pixels[i+2] = rgb[2]
        self.pixels[i+3] = a


    def set_sprite_nearest(self):
        texture = self.sprite.image.get_texture()

        glBindTexture(texture.target, texture.id)
        glTexParameteri(texture.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    @property
    def position(self):
        return self.pos_x, self.pos_y

    @property
    def centered_pos(self):
        sc = self.sprite.scale
        centered_x = self.pos_x - self.dim_x*sc / 2
        centered_y = self.pos_y - self.dim_y*sc / 2
        return centered_x, centered_y

    def update_sprite_pos(self):
        c_pos = self.centered_pos

        if self.camera is not None:
            vp = self.camera.get_position_on_viewport(c_pos[0], c_pos[1])
            self.sprite.scale = self.camera.zoom_scale
            self.sprite.x = vp[0]
            self.sprite.y = vp[1]
        elif self.centered:
            self.sprite.x = c_pos[0]
            self.sprite.y = c_pos[1]
        else:
            self.sprite.x = self.pos_x
            self.sprite.y = self.pos_y

    def set_sprite_scale(self, s):
        #will not work if you have a Camera on
        self.sprite.scale = s


    def update(self):

        self.image_data.set_data(self.format, self.pitch, bytes(self.pixels))
        self.sprite.image = self.image_data

        self.set_sprite_nearest()
        self.update_sprite_pos()
        if self.visible:
            self.sprite.draw()