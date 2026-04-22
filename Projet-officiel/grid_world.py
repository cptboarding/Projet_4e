import dataclasses as dc
from dataclasses import dataclass
import pyglet

from pyglet.gl import GL_NEAREST
from Tests import matrix_manager


@dataclass
class World:
    dimensions: tuple[int, int] = (150, 150)
    sq_size: float = 5.0
    position = [40, 40]
    world_matrix: list[list] = dc.field(default_factory=list[list])
    batch: pyglet.graphics.Batch = pyglet.graphics.Batch()

    def __post_init__(self):
        self.world_matrix = matrix_manager.create_matrix(self.dimensions)

    def __str__(self):
        return '\n'.join([str(i) for i in self.world_matrix])

    def update_screen(self):
        for y in range(self.dimensions[1]):
            for x in range(self.dimensions[0]):
                self.world_matrix[y][x].update_sq(self.position)

    def change_square(self, x, y, **kwargs):
        c = self.world_matrix[y][x]
        for k, value in kwargs.items():
            setattr(c, k, value)

    @dataclass
    class Square:
        type: str
        color: tuple[int, int, int]
        sq_size: float
        position: tuple[int, int]
        batch: pyglet.graphics.Batch
        __sq = pyglet.shapes.Rectangle(0, 0, 0, 0)

        def __post_init__(self):
            self.__sq = pyglet.shapes.Rectangle(
                self.position[0]*self.sq_size, self.position[1]*self.sq_size,
                self.sq_size, self.sq_size,
                color=self.color,
                batch=self.batch,
            )

        def update_sq(self):
            self.__sq.color = self.color

    @dataclass
    class TextureSquare:
        type: str
        position: tuple[int, int]
        img_size: float
        batch: pyglet.graphics.Batch
        image: pyglet.image.AbstractImage
        __sq = pyglet.sprite.Sprite

        def __post_init__(self):
            txt, resize = self.convert_texture()
            self.__sq = pyglet.sprite.Sprite(
                img=txt,
                x=self.position[0]*self.img_size, y=self.position[1]*self.img_size,
                batch=self.batch,
            )
            self.__sq.scale_x = resize[0]
            self.__sq.scale_y = resize[1]

        def convert_texture(self):
            texture = self.image.get_texture()
            texture.min_filter = GL_NEAREST
            texture.mag_filter = GL_NEAREST
            dim = [texture.width, texture.height]
            resize = [self.img_size/dim[0], self.img_size/dim[1]]
            return texture, resize

        def update_sq(self, world_pos):
            self.__sq.x = self.position[0] * self.img_size + world_pos[0]
            self.__sq.y = self.position[1] * self.img_size + world_pos[1]




if __name__ == "__main__":
    window = pyglet.window.Window()
    window.set_fullscreen(True)
    window.activate()

    from pyglet.window import key
    from Tests.key_handler import KeyHandler

    keys = KeyHandler(window)

    w = World(dimensions=(10, 10))

    @window.event
    def on_draw():
        window.clear()
        w.update_screen()
        w.batch.draw()

    def update(dt):
        global w
        if keys.key_just_pressed(key.UP):
            w.position[1] += 10
        if keys.key_just_pressed(key.DOWN):
            w.position[1] -= 10

    pyglet.clock.schedule_interval(update, 1 / 60.)

    pyglet.app.run()