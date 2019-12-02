# Created on 20 sSeptember 2019

from math import atan, cos, sin, copysign, pi


class Vector:
    def __init__(self, start, end, mag):
        self.start = start
        self.end = end
        self.mag = mag
        self.calc()

    def calc(self):
        self.delta = [self.end[0] - self.start[0], self.end[1] - self.start[1]]

        self.theta = atan(self.delta[1] / self.delta[0]) if self.delta[0] != 0 else pi / 2
        self.parts = [copysign(self.mag * cos(self.theta), self.delta[0]),
                      copysign(self.mag * sin(self.theta), self.delta[1])]

    def changeStart(self, start):
        self.start = start

    def changeEnd(self, end):
        self.end = end

    def changeMag(self, mag):
        self.mag = mag
