# Created on 20 September 2019

from circle import Circle
from sys import exit
import pygame
from pygame.locals import *
from math import atan

circles = [Circle(10), Circle(25), Circle(1), Circle(5)]

pygame.init()

display = pygame.display.set_mode((500, 500))

clicking = False
old_time = pygame.time.get_ticks()
while True:
    dt = pygame.time.get_ticks() - old_time
    old_time = pygame.time.get_ticks()

    display.fill((0, 0, 0))
    for c in circles:
        c.move(display, dt / 1000)

    events = pygame.event.get()
    for e in events:
        if e.type == MOUSEBUTTONDOWN and e.button == BUTTON_LEFT:
            clicking = True
            for c in circles:
                c.changeForce(c.click, None, pygame.mouse.get_pos(), 250 / c.r)
        elif e.type == MOUSEBUTTONUP and e.button == BUTTON_LEFT:
            clicking = False
            for c in circles:
                c.changeForce(c.click, None, None, 0)
            force = None
        elif e.type == MOUSEMOTION and clicking:
            for c in circles:
                c.changeForce(c.click, None, pygame.mouse.get_pos(), None)
        if e.type == QUIT:
            pygame.quit()
            exit(0)

    pygame.display.update()
