# Created on 18 September 2019

import pygame, sys
from pygame.locals import *
from random import randint
import time


class SnakeDriver:
    def __init__(self, dim, width):
        self.dim = dim
        self.width = width
        w, h = dim[0] * width, dim[1] * width
        self.board = Rect(0, 0, w, h)

        self.display = pygame.display.set_mode((w, h))
        pygame.display.set_caption("Yeet")

        self.shadow = pygame.Surface((w, h))
        self.shadow.set_alpha(128)
        self.repeat_rect = Rect(w * 9 / 20, h * 9 / 20, w / 10, h / 10)
        self.img = pygame.image.load("repeat.png")
        self.img = pygame.transform.scale(self.img, (self.repeat_rect.w, self.repeat_rect.h))

        self.setup()

    def setup(self):
        self.delta = (0, 0)
        self.direction = (0, 0)
        self.food = (0, 0)

        self.time = 0
        self.speed = 100

        self.snake = [(0, 0)]

        self.display.fill((0, 0, 0))
        for x in range(self.dim[0]):
            for y in range(self.dim[1]):
                self.update(None, (x, y))
        self.update(self.snake[0], None)
        self.spawn_food()

    def run(self, events, dt):
        self.time += dt
        if self.time >= self.speed and not self.delta == (0, 0):
            self.direction = self.delta
            last = self.snake[-1]
            new = (last[0] + self.delta[0], last[1] + self.delta[1])
            if self.board.collidepoint((new[0] * self.width, new[1] * self.width)):
                self.snake.append(new)
                self.update(new, self.spawn_food() if new == self.food else self.snake.pop(0))
                self.time = 0
                if self.snake.count(new) > 1:
                    return self.lose()
            else:
                return self.lose()

        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_LEFT and self.direction[0] != 1:
                    self.delta = (-1, 0)
                elif event.key == K_RIGHT and self.direction[0] != -1:
                    self.delta = (1, 0)
                elif event.key == K_UP and self.direction[1] != 1:
                    self.delta = (0, -1)
                elif event.key == K_DOWN and self.direction[1] != -1:
                    self.delta = (0, 1)
        return True

    def restart(self, events):
        for event in events:
            if event.type == MOUSEBUTTONUP and event.button == BUTTON_LEFT \
                    and self.repeat_rect.collidepoint(pygame.mouse.get_pos()):
                self.setup()
                return True
        return False

    def update(self, new, old):
        if old != None:
            rect = Rect(old[0] * self.width, old[1] * self.width, self.width, self.width)
            pygame.draw.rect(self.display, (128, 128, 128), rect.inflate(-self.width / 10, -self.width / 10))
        if new != None:
            rect = Rect(new[0] * self.width, new[1] * self.width, self.width, self.width)
            pygame.draw.rect(self.display, (0, 255, 0), rect.inflate(-self.width / 10, -self.width / 10))

    def spawn_food(self):
        self.food = randCoord(0, 0, self.dim[0], self.dim[1])
        while self.food in self.snake:
            self.food = randCoord(0, 0, self.dim[0], self.dim[1])
        rect = Rect(self.food[0] * self.width, self.food[1] * self.width, self.width, self.width)
        pygame.draw.rect(self.display, (255, 0, 0), rect.inflate(-self.width / 10, -self.width / 10))

    def lose(self):
        self.display.blit(self.shadow, (0, 0))
        pygame.draw.rect(self.display, (200, 200, 200), self.repeat_rect)
        self.display.blit(self.img, (self.repeat_rect.x, self.repeat_rect.y))
        return False


# Generates a random coord with minX <= x < maxX and minY <= y < maxY
def randCoord(minX, minY, maxX, maxY):
    return (randint(minX, maxX - 1), randint(minY, maxY - 1))
