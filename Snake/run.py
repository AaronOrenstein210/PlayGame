# Created on 18 September 2019

from SnakeDriver import SnakeDriver
from sys import exit
from pygame.display import update
from pygame.event import get as get_events
from pygame.time import get_ticks
from pygame import init, quit
from pygame.locals import QUIT

width = 25
dim = (25, 25)

init()
driver = SnakeDriver(dim, width)

playing = True
old_time = get_ticks()
while True:
    dt = get_ticks() - old_time
    old_time = get_ticks()

    events = get_events()
    event_types = [e.type for e in events]
    if QUIT in event_types:
        quit()
        exit(0)

    if playing:
        playing = driver.run(events, dt)
    else:
        playing = driver.restart(events)

    update()
