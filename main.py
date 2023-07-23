import threading
import time

import pygame
import game

pygame.init()

clock = pygame.time.Clock()

size = (0, 0)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
size = screen.get_size()

game = game.Game(screen)
run = True

class PeriodicSleeper(threading.Thread):
    def __init__(self, task_function, period):
        super().__init__()
        self.task_function = task_function
        self.period = period
        self.i = 0
        self.t0 = time.time()
        self.start()

    def sleep(self):
        self.i += 1
        delta = self.t0 + self.period * self.i - time.time()
        if delta > 0:
            time.sleep(delta)

    def run(self):
        while 1:
            self.task_function()
            self.sleep()

if run:
    sleeper = PeriodicSleeper(game.update_time, 0.01)

while run:

    run = game.run

    clock.tick(60)
    game.draw()
    game.update()

pygame.quit()