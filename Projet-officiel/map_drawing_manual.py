
"""
First docstring in my life duh

Program that lets you manually draw a map for the game, the main project
"""

import pyglet
import math

from SquareMap import SquareMap as Square
from Camera import Camera


def floored_to(x, n):
    return n*math.floor(x/n)


def main():

    map_size = (50, 50)
    tile_size = 4
    map_base_size = 5.0

    drawing_mode = "tangent"

    cam = Camera((1000, 1000))
    cam.debug_ui()

    s = Square(cam, "game", layer=0, map_dimensions=map_size, map_pixel_size=tile_size, size=map_base_size)
    s.rand_test()
    cam.window_objects.append(s)

    pointer = Square(cam, "game", layer=0, map_dimensions=(1, 1), map_pixel_size=tile_size, size=map_base_size, centered=False)
    pointer.rand_test()
    pointer.set_pixel((0, 0), (0, 0, 255))
    cam.window_objects.append(pointer)

    @cam.window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        #draw tangent
        if cam.mouse_left:
            if drawing_mode == "tangent":
                tangent_drawing(x, y, dx, dy)
            elif drawing_mode == "point":
                point_drawing(int(x), int(y))

    def edit_point(x, y, rgb):
        max_id = map_size
        if 0 <= x < max_id[0] and 0 <= y < max_id[1]:
            s.set_pixel((x, y), (0, 0, 255))

    def draw_square(x: int, y: int, rgb, size=2):
        edit_point(x, y, rgb) #center
        for i in range(1, size):
            l = 1 + 2 * i
            xp = x - i
            yp = y - i
            d = 1
            for n in range(2):
                for _ in range(l-1):
                    yp += 1 * d
                    edit_point(xp, yp, rgb)
                for _ in range(l-1):
                    xp += 1 * d
                    edit_point(xp, yp, rgb)
                d *= -1

    def point_drawing(x: int, y: int):
        max_id = map_size
        xx, yy = mouse_pos_viewport_transform(x, y)
        x_id, y_id = find_mouse_id(xx, yy)
        draw_square(x_id, y_id, (0, 0, 255), size=1)

    def tangent_drawing(x, y, dx, dy):
        X1, Y1 = mouse_pos_viewport_transform(x - dx, y - dy)
        X2, Y2 = mouse_pos_viewport_transform(x, y)
        x1_id, y1_id = find_mouse_id(X1, Y1)
        x2_id, y2_id = find_mouse_id(X2, Y2)

        # number of tiles in between + the sign
        dx_id_s = x2_id - x1_id
        dy_id_s = y2_id - y1_id
        dx_id = abs(dx_id_s)
        dy_id = abs(dy_id_s)

        r: dict = {}  # {x: y}

        if dx_id == 0 or dy_id == 0:
            if dx_id == 0 and dy_id == 0:
                pass
            elif dx_id == 0 and dy_id != 0:
                dy_s = int(dy_id / (y2_id - y1_id))
                for i in range(0, (dy_id + 1) * dy_s, dy_s):
                    r[x1_id] = y1_id + i
            elif dx_id != 0 and dy_id == 0:
                dx_s = int(dx_id / (x2_id - x1_id))
                for i in range(0, (dx_id + 1) * dx_s, dx_s):
                    r[x1_id + i] = y1_id

        else:
            dx_s = int(dx_id / (x2_id - x1_id))
            dy_s = int(dy_id / (y2_id - y1_id))

            if dx_id >= dy_id:
                tng = dy_id * dy_s / dx_id  # the abs tangent always smaller than 1
                for i in range(0, (dx_id + 1) * dx_s, dx_s):
                    r[x1_id + i] = y1_id + round(tng * abs(i))
            else:
                tng = dx_id * dx_s / dy_id  # the abs tangent always smaller than 1
                for i in range(0, (dy_id + 1) * dy_s, dy_s):
                    r[x1_id + round(tng * abs(i))] = y1_id + i

        for i in r.keys():
            xx = i
            yy = r[i]
            max_id = map_size
            if 0 <= xx < max_id[0] and 0 <= yy < max_id[1]:
                s.set_pixel((xx, yy), (0, 0, 255))

    def tile_len():
        return s.tile_size / cam.zoom_scale

    def mouse_pos_viewport():
        x = cam.pos_x + (cam.window._mouse_x - cam.window_center[0]) / cam.zoom_scale
        y = cam.pos_y + (cam.window._mouse_y - cam.window_center[1]) / cam.zoom_scale
        return x, y

    def mouse_pos_viewport_transform(mx, my):
        x = cam.pos_x + (mx - cam.window_center[0]) / cam.zoom_scale
        y = cam.pos_y + (my - cam.window_center[1]) / cam.zoom_scale
        return x, y


    def find_mouse_id(x, y):
        t_len = tile_len()
        dc = s.downside_corner

        x_id = int(math.floor((x - dc[0]) / t_len))
        y_id = int(math.floor((y - dc[1]) / t_len))

        return x_id, y_id

    def update(dt):
        dc = s.downside_corner
        t_len = tile_len()
        x, y = mouse_pos_viewport()
        x_id, y_id = find_mouse_id(x, y)
        max_id = map_size

        #pointer animation
        if 0 <= x_id < max_id[0] and 0 <= y_id < max_id[1]:
            px, py = dc[0] + x_id*t_len, dc[1] + y_id*t_len
            pointer.pos_x, pointer.pos_y = [px, py]
            if cam.mouse_left:
                print("ppp")
                point_drawing(int(px), int(py))


    pyglet.clock.schedule_interval(update, 1/60.0)

    pyglet.app.run()

main()