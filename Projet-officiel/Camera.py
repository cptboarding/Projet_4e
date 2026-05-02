
"""
Wow a docstring, try to get over it

Basically a camera module for pyglet
One Camera supported at a time
The Camera automatically runs the pyglet window so just put the stuff inside
"""


from typing import Callable

import pyglet
from pyglet.window import key


class Camera:

    def __init__(self,
                 viewport_dim: tuple[int, int],
                 centered: bool = True,
                 update_fps: int = 60,
                 start_zoom: float = 1,
                 start_pos: tuple[int, int] = (0, 0),
                 ):

        self.viewport_dimensions = viewport_dim
        self.centered = centered

        self.zoom_scale = start_zoom
        self.pos_x = start_pos[0]
        self.pos_y = start_pos[1]

        """The thing below initializes the pyglet window"""

        #window creation
        self.window = pyglet.window.Window(width=self.viewport_dimensions[0], height=self.viewport_dimensions[0])
        self.update_fps = update_fps

        """
        This one push below pushes the class itself so that the window can see the on_draw() inside the class instead of
        having an @self.window.event and def on_draw() inside the __init__() (an alternative).
        Also, tan(q) Gemini for your humble contribution
        """
        self.window.push_handlers(self)

        #updater function
        pyglet.clock.schedule_interval(self.update, 1.0/self.update_fps)

        #necessary key handlers
        self.keys = key.KeyStateHandler()
        self.window.push_handlers(self.keys)

        #create list dumps for the drawing time, either object or UI element
        self.window_objects = []
        self.window_UI_static = []
        self.window_UI_dynamic = []


    #window process --------------------------------------------------------------

    class DynamicWrapper:
        def __init__(self, obj: pyglet, camera: "Camera", updater_func: Callable[[pyglet, "Camera"], None]):
            self.obj = obj
            self.camera = camera
            self.updater = updater_func

        def draw(self):
            self.obj.draw()

        def update(self):
            self.updater(self.obj, self.camera)

    #some basic UI used for previous tests, grew attached to it
    def debug_ui(self):
        #region Labels
        scroll_label = pyglet.text.Label(
            'Zoom value debug',
            x=10,
            y=self.window.height - 10,
            anchor_x='left',
            anchor_y='top'
        )
        cam_pos_label = pyglet.text.Label(
            'Cam pos debug',
            x=10,
            y=self.window.height - 50,
            anchor_x='left',
            anchor_y='top'
        )

        crosshair = pyglet.text.Label(
            '+',
            x=int(self.window.width / 2.0),
            y=int(self.window.height / 2.0),
            anchor_x='center',
            anchor_y='center',
            font_size=30,
        )
        # endregion

        #region some behavior definitions
        def scroll_label_updater(obj: pyglet, camera: "Camera"):
            obj.text = f"Scroll: {camera.zoom_scale:.1f}"
        dynamic_scroll_label = self.DynamicWrapper(scroll_label, self, scroll_label_updater)

        def cam_pos_label_updater(obj: pyglet, camera: "Camera"):
            obj.text = f"Camera pos: ({cam.pos_x:.1f}, {cam.pos_y:.1f})"
        dynamic_cam_pos_label = self.DynamicWrapper(cam_pos_label, self, cam_pos_label_updater)
        #endregion

        static = [crosshair]
        dynamic = [dynamic_scroll_label, dynamic_cam_pos_label]

        self.window_UI_static += static
        self.window_UI_dynamic += dynamic

    #region Update Exceptions
    #if you are trying to draw something else than a pyglet feature
    class DrawingError(Exception):
        def __init__(self, message="The drawn object is not a pyglet one"):
            print(self.__name__, ": ", message)

    #If the UI object is not this shady wrapper
    class DynamicWrapperError(Exception):
        def __init__(self, message="You spoiled the dynamic UI objects list with something else"):
            print(self.__name__, ": ", message)

    #If an object on screen has no updater
    class ObjectUpdateError(Exception):
        def __init__(self, message="Trying to update an object with no update() function"):
            print(self.__name__, ": ", message)
    #endregion

    #runtime function
    def on_draw(self):
        self.window.clear()
        #>>>put some updater script here<<<

        #region Updaters
        #on-screen objects, require an update() function that draws by itself
        #made for complex objects that are not directly pyglet ones, that for example require position
        for obj in self.window_objects:
            for dn in self.window_UI_dynamic:
                try:
                    obj.update()
                except:
                    raise self.ObjectUpdateError
        #plain draw, no updating
        for st in self.window_UI_static:
            try:
                st.draw()
            except:
                raise self.DrawingError
        #for dynamic text or other stuff
        for dn in self.window_UI_dynamic:
            try:
                dn.update()
            except:
                raise self.DynamicWrapperError
            else:
                try:
                    dn.draw()
                except:
                    raise self.DrawingError
        #endregion

    #scroll in runtime
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.scroll_handler(scroll_y)

    def update(self, dt):
        self.position_handler(keyhandler=self.keys)


    #the shit ive been sweating on all this time -----------------------------
    #get the position on screen

    @property
    def window_center(self):
        return self.viewport_dimensions[0]/2.0, self.viewport_dimensions[1]/2.0

    @property
    def base_position(self):
        return self.pos_x, self.pos_y

    def get_position_on_viewport(self, x, y, img_offset: tuple[float, float] = (0, 0)):
        vp = self.base_position
        c = self.window_center
        return (
            (x - vp[0]) * self.zoom_scale + c[0] + img_offset[0],
            (y - vp[1]) * self.zoom_scale + c[1] + img_offset[1],
        )

    #UI handling --------------------------------------------------------------

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


if __name__ == "__main__":

    dim = (1000, 1000)
    cam = Camera(dim)
    cam.debug_ui()

    s = Square.Square(cam)
    cam.window_objects.append(s)

    pyglet.app.run()
