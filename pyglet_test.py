
import pyglet
from pyglet.window import key
from pyglet.window import mouse


window = pyglet.window.Window()
window.set_fullscreen(True)


label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

label2 = pyglet.text.Label('Boo',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

l = label
image = pyglet.image.load('ziak.jpg')
image.anchor_x = image.width // 2
image.anchor_y = image.height // 2


batch = pyglet.graphics.Batch()

sp = pyglet.sprite.Sprite(img=image, x=500, y=400, batch=batch)
sp.scale_x = -1


sprites = [
    sp,
]


def update(dt):
    pass

pyglet.clock.schedule_interval(update, 1/60.)


@window.event
def on_draw():
    window.clear()
    l.draw()
    batch.draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.B:
        global l
        l = label2
    if modifiers == key.MOD_CTRL and symbol == key.Q:
        pyglet.app.exit()

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        global sp
        sp.scale_x *= -1

ziak = pyglet.resource.media('fixette.mp3')
ms = pyglet.resource.media('booskhalloween.mp3')


event_logger = pyglet.window.event.WindowEventLogger()
#window.push_handlers(event_logger)
pyglet.app.run()