# Created on 13 November 2019
# Runs the program

from sys import path
from os import chdir
from sys import exit
import pygame
from pygame.locals import *
from scripts.GameLayout import GameLayout

CHOOSING, READING = 0, 1
display, game_layout = None, None


def main():
    global display, game_layout

    pygame.init()

    game = None

    display = pygame.display.set_mode((500, 500), RESIZABLE)

    game_layout = GameLayout()
    display.blit(game_layout.surface, (0, 0))

    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                exit(0)
            elif e.type == VIDEORESIZE:
                display = pygame.display.set_mode((max(e.w, 250), max(e.h, 250)), RESIZABLE)
                game_layout.load_games()
                if game is None:
                    display.blit(game_layout.surface, (0, 0))
                else:
                    game.get_description()
            elif e.type == MOUSEBUTTONUP:
                if e.button == BUTTON_WHEELUP or e.button == BUTTON_WHEELDOWN:
                    display.fill((0, 0, 0))
                    if game is None:
                        game_layout.move(e.button == BUTTON_WHEELUP)
                    else:
                        game.description.do_scroll(e.button == BUTTON_WHEELUP)
                elif e.button == BUTTON_LEFT:
                    pos = pygame.mouse.get_pos()
                    if game is None:
                        game = game_layout.click(pos)
                        if game is not None:
                            game.get_description()
                    else:
                        result = game.description.click(pos)
                        if result == "action":
                            if pos[0] <= display.get_size()[0] / 2:
                                start_game(game.name)
                            else:
                                display.fill((0, 0, 0))
                                display.blit(game_layout.surface, (0, game_layout.off))
                            game = None
        pygame.display.flip()


def start_game(game):
    pygame.quit()
    path.insert(0, path[0] + "\\" + game)
    chdir(game)
    try:
        exec(open("run.py").read())
    except SystemExit:
        print("Exited")
    # Tear Down
    chdir("../")
    path.pop(0)
    # Reset state
    pygame.init()
    global display
    display = pygame.display.set_mode((500, 500), RESIZABLE)
    display.blit(game_layout.surface, (0, game_layout.off))


main()
