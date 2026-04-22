import tkinter as tk

screen_dim = [500, 500]
pix_num = [100, 100]
pix_size = [screen_dim[0]/pix_num[0], screen_dim[1]/pix_num[1]]

def matrix(dim):
    l = []
    ll = []
    for i in range(dim[0]):
        ll.append(0)
    for i in range(dim[1]):
        l.append(ll)
    return l

m = matrix(pix_num)

def main():
    root = tk.Tk()
    root.geometry(f'{screen_dim[0]}x{screen_dim[1]}')

    
    root.mainloop()