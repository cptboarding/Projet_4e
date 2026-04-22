
import pyglet

class KeyHandler:

    def __init__(self, window: pyglet.window.Window):
        self.window = window
        self.pressed_keys: set = set()
        self.just_pressed_keys: set = set()

        @window.event
        def on_key_press(symbol, modifiers):
            self.pressed_keys.add(symbol)
            self.just_pressed_keys.add(symbol)
            pyglet.clock.schedule_once(lambda dt: key_timeout(symbol), 1/60.)

        @window.event
        def on_key_release(symbol, modifiers):
            self.pressed_keys.discard(symbol)
            key_timeout(symbol)

        def key_timeout(k):
            if k in self.pressed_keys:
                self.just_pressed_keys.discard(k)

    def key_pressed(self, arg: pyglet.window.key) -> bool:
        return arg in self.pressed_keys

    def key_just_pressed(self, arg: pyglet.window.key) -> bool:
        return arg in self.just_pressed_keys