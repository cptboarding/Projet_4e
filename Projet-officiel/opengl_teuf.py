
import pyglet
from pyglet.gl import *
import numpy as np
import random

window = pyglet.window.Window(800, 600)

# Chunk / tile setup
TILE_SIZE = 1
CHUNK_W, CHUNK_H = 512, 512
WIDTH, HEIGHT = CHUNK_W*TILE_SIZE, CHUNK_H*TILE_SIZE

pixels = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
pixels[:, :] = [50, 50, 50, 255]  # gray background

# Create texture AFTER window exists
image = pyglet.image.ImageData(WIDTH, HEIGHT, 'RGBA', pixels.tobytes())
texture = image.get_texture()
sprite = pyglet.sprite.Sprite(texture, x=100, y=100)

def update_tile(tx, ty, color):
    px, py = tx*TILE_SIZE, ty*TILE_SIZE
    pixels[py:py+TILE_SIZE, px:px+TILE_SIZE] = color

    glBindTexture(GL_TEXTURE_2D, texture.id)  # must bind
    glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, WIDTH, HEIGHT,
                    GL_RGBA, GL_UNSIGNED_BYTE, pixels.ctypes.data)

# Schedule a test tile update after window/context is ready
def test_update(dt):
    red = [255, 0, 0, 255]
    black = [50, 50, 50, 255]
    for y in range(CHUNK_H):
        for x in range(CHUNK_W):
            if x % 2 == 1:
                update_tile(x, y, red)
            else:
                update_tile(x, y, black)

#pyglet.clock.schedule_interval(test_update, 1)  # run after 0.1s

@window.event
def on_draw():
    window.clear()
    sprite.draw()

pyglet.app.run()