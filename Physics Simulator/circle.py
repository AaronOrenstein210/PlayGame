# Created on 20 September 2019

import pygame
from math import ceil, sqrt, pi
from random import randint
from vector import Vector


class Circle:
    def __init__(self, r):
        self.r = r
        self.coord = [r, r]
        self.v = [0, 0]
        self.a = [0, 0]
        self.drag = Vector(self.coord, self.coord, 0)
        self.click = Vector(self.coord, self.coord, 0)
        self.time = 0
        color_vals = (0, 128, 255)
        self.color = (color_vals[randint(0, 2)], color_vals[randint(0, 2)], color_vals[randint(0, 2)])

    def move(self, display, dt):
        self.time += dt
        if self.time >= .01:
            # For x and y
            for i in (0, 1):
                # Calculate new position and velocity (1m = 10px)
                self.coord[i] += 10 * ((self.v[i] * self.time) +
                                       (self.a[i] * pow(self.time, 2) / 2))
                self.v[i] += self.a[i] * self.time
                # Check if we hit an edge
                self.checkEdge(display.get_size())

            self.changeForce(self.drag, self.coord,
                             (self.coord[0] - self.v[0], self.coord[1] - self.v[1]),
                             .1 * distanceFrom((0, 0), self.v))
            self.changeForce(self.click, self.coord, None, None)
            self.time = 0

        pygame.draw.circle(display, self.color, (ceil(self.coord[0]), ceil(self.coord[1])), self.r)

    def checkEdge(self, dim):
        for i in (0, 1):
            if self.coord[i] < self.r:
                self.coord[i] = self.r
                self.v[i] *= -1
            elif self.coord[i] > dim[i] - self.r:
                self.coord[i] = dim[i] - self.r
                self.v[i] *= -1

    def changeForce(self, force, start, end, mag):
        if start != None:
            force.changeStart(start)
        if end != None:
            force.changeEnd(end)
        if mag != None:
            force.changeMag(mag)

        self.a[0] -= force.parts[0]
        self.a[1] -= force.parts[1]
        force.calc()
        self.a[0] += force.parts[0]
        self.a[1] += force.parts[1]


def distanceFrom(start, end):
    return sqrt(pow(start[0] - end[0], 2) + pow(start[1] - end[1], 2))
