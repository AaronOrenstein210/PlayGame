# Created on 13 November 2019

from os import listdir
from os.path import isfile, isdir, join
from pygame import Surface, Rect
from pygame.display import get_surface
from scripts.Game import Game
from scripts.functions import get_scaled_font, get_widest_string


class GameLayout:
    def __init__(self):
        self.h = 0
        self.off, self.max_off = 0, 0
        self.surface = Surface((0, 0))
        self.games = [Game(name) for name in listdir("./") if
                      isdir(join("./", name)) and isfile(join(name + "/run.py"))]
        self.rects = {}
        self.load_games()

    def move(self, up):
        if up:
            self.off = min(0, self.off + int(self.h / 10))
        else:
            self.off = max(self.max_off, self.off - int(self.h / 10))
        get_surface().fill((0, 0, 0))
        get_surface().blit(self.surface, (0, self.off))

    def load_games(self):
        dim = get_surface().get_size()
        # Set up length variables
        item_h = max(25, int(dim[1] / 10))
        item_w = max(50, dim[0] - item_h)
        dim = (item_w + item_h, dim[1])
        self.h = item_h * len(self.games)
        # Create font
        names = [g.name for g in self.games]
        font = get_scaled_font(item_w, item_h, get_widest_string(names, "Times New Roman"), "Times New Roman")
        # Create surface
        self.surface = Surface((dim[0], self.h))
        # Draw on all items
        self.rects.clear()
        for idx, game in enumerate(self.games):
            # Create the click rectangle
            r = Rect(0, idx * item_h, dim[0] - item_h, item_h)
            # Draw text
            self.surface.blit(game.get_display(r.size, font), r)
            self.rects[game] = r
        self.max_off = min(0, dim[1] - self.h)

    def click(self, p):
        p = (p[0], p[1] - self.off)
        for game in self.games:
            if self.rects[game].collidepoint(p):
                return game
