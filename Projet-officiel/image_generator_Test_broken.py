

import pyglet
from Tests import useful_stuff as us
import random
from pyglet.window import mouse


class MapImage:

    def __init__(self, dimensions: tuple[int, int]):
        self.dimensions = dimensions
        self.buffer = bytearray(dimensions[0] * dimensions[1] * 4)
        self.texture = pyglet.image.Texture.create(self.dimensions[0], self.dimensions[1])
        self.image = pyglet.image.ImageData(self.dimensions[0], self.dimensions[1], "RGBA", self.buffer)
        self.texture.blit_into(self.image, 0, 0, 0)
        self.sprite = pyglet.sprite.Sprite(self.texture)
        self.scale = 1
        self.position = [100, 100]
        self.drag_anchor = self.position
        self.mouse_delta = [0, 0]



    def setpixel(self, pos: tuple[int, int], rgb: tuple[int, int, int], a: int = 255):
        x = pos[0]
        y = pos[1]
        i = (y*self.dimensions[0] + x) * 4

        self.buffer[i] = rgb[0]
        self.buffer[i+1] = rgb[1]
        self.buffer[i+2] = rgb[2]
        self.buffer[i+3] = a

    def update_sprite_pos(self):
        self.sprite.x = self.position[0]
        self.sprite.y = self.position[1]

    def generate_image(self):
        self.texture.blit_into(self.image, 0, 0, 0)
        self.sprite.image = self.texture
        self.sprite.scale = self.scale

press = False
@us.debugger
def main():
    window = pyglet.window.Window(width=1000, height=1000)
    window.activate()

    map = MapImage((100, 100))



    def rand_test(dt=0):
        for y in range(100):
            for x in range(100):
                map.setpixel((x, y), (255*random.randint(0, 1), 0, 0))
        map.generate_image()
    rand_test()

    pyglet.clock.schedule_interval(rand_test, 0.1)

    @window.event
    def on_draw():
        window.clear()
        map.update_sprite_pos()
        map.sprite.draw()
        print(map.sprite.position)
        x, y = window._mouse_x, window._mouse_y
        if press:
            map.position[0] = x - map.drag_anchor[0]
            map.position[1] = y - map.drag_anchor[1]


    @window.event
    def on_mouse_scroll(x, y, scroll_x, scroll_y):
        if map.scale > 1 and scroll_y < 0:
            map.scale += scroll_y/10
        if map.scale < 5 and scroll_y > 0:
            map.scale += scroll_y/10

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        if button == mouse.LEFT:
            print("s")
            press = True
            map.drag_anchor = [
                map.position[0]-x,
                map.position[1]-y
            ]

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        if button == mouse.LEFT:
            press = False

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        print(x, "/", y)




    pyglet.app.run()

    print("yatta")