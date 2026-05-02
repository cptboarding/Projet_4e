
"""
First docstring in my life duh

Program that lets you manually draw a map for the game, useful for debug
"""

import pyglet
from pyglet.window import key
from pyglet.window import mouse

import math
from Tests import tile_data_converter as Converter

#the map generator to show us what we draw
import Square_map as Square

def main():

    #globals
    global_scale = 10.0
    map_size = [50, 50]
    window_size = [1000, 1000]

    origin = [0, 0]
    center = [i/2 for i in window_size]
    downside_corner = [win/2 - mp*global_scale/2 for win, mp in zip(window_size, map_size)]
    upside_corner = [win-dwn for dwn, win in zip(downside_corner, window_size)]

    #main square map
    s = Square.Square(x_dim=map_size[0], y_dim=map_size[1])
    s.set_sprite_scale(global_scale)
    s.pos_x, s.pos_y = center
    s.rand_test()

    #square for mouse position
    pointer = Square.Square(x_dim=1, y_dim=1)
    pointer.centered = False
    pointer.set_sprite_scale(global_scale)
    pointer.set_pixel((0, 0), (0, 255, 0))
    pointer.pos_x, pointer.pos_y = [100, 100]

    #window
    window = pyglet.window.Window(width=window_size[0], height=window_size[1])
    handler = mouse.MouseStateHandler()
    window.push_handlers(handler)

    @window.event
    def on_draw():
        window.clear()
        s.update()
        pointer.update()

    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == key.SPACE:
            print(f'Map data (copy-paste the following):\n{s.pixels}')
            d = Converter.Decoder()
            e = Converter.Encoder()
            decoded = d.full_decode(s.pixels)
            print(f'decoded = {decoded}')
            encoded = e.full_encode(decoded)
            print(f'encoded  = {encoded}')
            print(f'original = {s.pixels}')
            print(encoded == s.pixels)

    def update(dt):

        x, y = window._mouse_x, window._mouse_y
        rx, ry = 10*math.floor(x/10), 10*math.floor(y/10)
        x_id = int((rx - downside_corner[0]) / global_scale)
        y_id = int((ry - downside_corner[1]) / global_scale)

        if 0 <= x_id < map_size[0] and 0 <= y_id < map_size[1]:
            pointer.visible = True
            pointer.pos_x, pointer.pos_y = [rx, ry]

            if handler[mouse.LEFT]:
                s.set_pixel((x_id, y_id), (0, 0, 255))
        else:
            pointer.visible = False



    pyglet.clock.schedule_interval(update, 1 / 60)
    pyglet.app.run(1/60)


main()