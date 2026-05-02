
import pyglet
import random

from pyglet.gl import *
from pyglet.window import key
import Square_map as Square


class Camera:

    def __init__(self):
        self.viewport_dimensions = (1000, 1000)
        self.centered = True


        self.zoom_scale = 1
        self.pos_x = 0
        self.pos_y = 0

    @property
    def window_center(self):
        return self.viewport_dimensions[0]/2.0, self.viewport_dimensions[1]/2.0

    @property
    def viewport_position(self):
        dx = 0
        dy = 0
        if self.centered:
            dx += self.viewport_dimensions[0]/2.0
            dy += self.viewport_dimensions[1]/2.0
        return (-1 * self.pos_x + dx,
                -1 * self.pos_y + dy)

    @property
    def base_position(self):
        return [self.pos_x, self.pos_y]

    def get_position_on_viewport(self, x, y):
        vp = self.base_position
        c = self.window_center
        return (
            (x - vp[0]) * self.zoom_scale + c[0],
            (y - vp[1]) * self.zoom_scale + c[1],
        )

    def scroll_handler(self, scroll_y, lims: tuple[float, float] = (0.6, 10)):
        if scroll_y != 0:
            if scroll_y > 0 and self.zoom_scale < lims[1]:
                self.zoom_scale += 0.1
            elif scroll_y < 0 and lims[0] < self.zoom_scale:
                self.zoom_scale -= 0.1

    def position_handler(self, keyhandler):
        if keyhandler[key.UP]:
            self.pos_y += 10
        if keyhandler[key.DOWN]:
            self.pos_y -= 10
        if keyhandler[key.RIGHT]:
            self.pos_x += 10
        if keyhandler[key.LEFT]:
            self.pos_x -= 10


class StaticImage:

    def __init__(self, viewport, path, centered=True):

        self.camera = viewport

        self.img = pyglet.image.load(path)
        self.sprite = pyglet.sprite.Sprite(self.img)

        self.offset = (0, 0)
        if centered:
            self.offset = (self.img.width/2, self.img.height/2)


    def update(self):
        vp = self.camera.viewport_position
        self.sprite.scale = self.camera.zoom_scale
        self.sprite.x = vp[0] - self.offset[0]
        self.sprite.y = vp[1] - self.offset[1]

        self.sprite.draw()


window = pyglet.window.Window(width=1000, height=1000)

keys = key.KeyStateHandler()
window.push_handlers(keys)

cam = Camera()

s = Square.Square(cam)
s.rand_test()

#region Labels
scroll_label = pyglet.text.Label(
	'Debug text',
	x=10,
	y=window.height - 10,
	anchor_x='left',
	anchor_y='top'
)
size_label = pyglet.text.Label(
	'Debug text',
	x=10,
	y=window.height - 30,
	anchor_x='left',
	anchor_y='top'
)
cam_pos_label = pyglet.text.Label(
	'Debug text',
	x=10,
	y=window.height - 50,
	anchor_x='left',
	anchor_y='top'
)
img_pos_label = pyglet.text.Label(
	'Debug text',
	x=10,
	y=window.height - 70,
	anchor_x='left',
	anchor_y='top'
)
pos_ratio_label = pyglet.text.Label(
	'Debug text',
	x=10,
	y=window.height - 90,
	anchor_x='left',
	anchor_y='top'
)
crosshair = pyglet.text.Label(
	'+',
	x=window.width/2,
	y=window.height/2,
	anchor_x='center',
	anchor_y='center',
    font_size=30,
)
#endregion


@window.event
def on_draw():
    window.clear()
    s.update()

    #labels
    scroll_label.text = f"Scroll: {cam.zoom_scale:.1f}"
    scroll_label.draw()
    size_label.text = f"Sprite size multiplier: {s.sprite.scale:.1f}"
    size_label.draw()
    cam_pos_label.text = f"Camera pos: ({cam.pos_x:.1f}, {cam.pos_y:.1f})"
    cam_pos_label.draw()
    img_pos_label.text = f"Image pos: ({s.pos_x:.1f}, {s.pos_y:.1f})"
    img_pos_label.draw()
    crosshair.draw()

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    cam.scroll_handler(scroll_y)


def update(dt):
    cam.position_handler(keys)

pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()


