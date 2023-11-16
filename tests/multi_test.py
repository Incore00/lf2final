#!/usr/bin/env python
""" pg.examples.video

Experimental!

* dialog message boxes with messagebox.
* multiple windows with Window
* driver selection
* Renderer, Texture, and Image classes
* Drawing lines, rects, and such onto Renderers.
"""
import os
import pygame as pg
from pygame._sdl2 import Window, Texture, Image, Renderer, get_drivers, messagebox

data_dir = os.path.join(os.path.split(os.path.abspath(__file__))[0], "data")


def load_img(file):
    return pg.image.load(os.path.join(data_dir, file))


pg.display.init()
pg.key.set_repeat(1000, 10)



win = Window("asdf", resizable=True)

running = True


win2 = Window("2nd window", size=(256, 256), always_on_top=True)



while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif getattr(event, "window", None) == win2:
            if (
                event.type == pg.KEYDOWN
                and event.key == pg.K_ESCAPE
                or event.type == pg.WINDOWCLOSE
            ):
                win2.destroy()

pg.quit()