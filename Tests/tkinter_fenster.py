
import tkinter as tk
from dataclasses import dataclass


@dataclass
class Screen:
    screen_dim = [1000, 1000]
    pixels_num = [50, 50]
    screen_mx = []
    colors = ['white', 'black']

    def __post_init__(self):
        self.pixel_size = [self.screen_dim[0]/self.pixels_num[0], self.screen_dim[1]/self.pixels_num[1]]
        self.screen_mx = self.matrix(self.pixels_num)

    @staticmethod
    def matrix(dim: list):
        l = [[i2 % 2 for i2 in range(dim[0])] for i in range(dim[1])]
        return l

    def change_cell(self, color_id: int, x: int, y: int):
        self.screen_mx[y][x] = color_id

    def main(self):
        root = tk.Tk()
        root.geometry(f'{self.screen_dim[0]}x{self.screen_dim[1]}')
        frame_container = []

        for y in range(self.pixels_num[1]):
            print('y= ', y)
            for x in range(self.pixels_num[0]):
                print('x= ', x)
                frame_container.append(
                    tk.Frame(root, bg=self.colors[self.screen_mx[y][x]])
                )
                frame_container[-1].place(
                    x=self.pixel_size[0]*(x),
                    y=self.pixel_size[1]*(y),
                    width=self.pixel_size[0],
                    height=self.pixel_size[1],
                )

        root.mainloop()


if __name__ == '__main__':
    s = Screen()
    s.main()
