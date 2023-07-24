import datetime
import pygame

import fileutils
from scramblegenerator import clock

class Game:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.run = True

        self.font = pygame.font.Font("font.ttf", 25)
        self.big_font = pygame.font.Font("font.ttf", 100)

        self.current_scramble = ""
        self.current_puzzle = "clock"

        self.formatted_time = ""

        self.started = False
        self.ready = 0
        self.time_10ms = 0

        self.refresh()

    def refresh(self):

        if self.current_puzzle == "clock":
            self.current_scramble = clock.get_scramble()

    def update(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.run = False
                return

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.run = False
                    return

                if event.key == pygame.K_r:
                    if not self.started: # avoid refreshing scrambles while timer is active
                        self.refresh()

                if event.key == pygame.K_SPACE:
                    if self.started:
                        fileutils.write_history(f"1.cth", self.formatted_time, self.current_scramble)
                        self.started = False # to stop the timer

        if not self.started:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.ready += 1
            else:
                if self.ready >= 20: # start the timer
                    self.time_10ms = 0
                    self.started = True

                self.ready = 0

    def update_time(self):

        if self.started:
            self.time_10ms += 1


    def draw(self):

        screen = self.screen
        screen.fill((0, 0, 0))

        if not self.started and self.ready <= 0:
            self.draw_text(self.current_scramble, (255, 255, 255), (10, 10))  # draw scramble on idle

        ms_datetime = datetime.datetime.fromtimestamp(self.time_10ms / 100.0) - datetime.timedelta(hours=1) # very weird

        if self.time_10ms < 1000:
            self.formatted_time = datetime.datetime.strftime(ms_datetime, "%S.%f")[:-4][1:]
        elif 1000 < self.time_10ms < 6000:
            self.formatted_time = datetime.datetime.strftime(ms_datetime, "%S.%f")[:-4]
        elif 6000 < self.time_10ms < 60000:
            self.formatted_time = datetime.datetime.strftime(ms_datetime, "%M:%S.%f")[:-4][1:]
        elif 60000 < self.time_10ms < 360000:
            self.formatted_time = datetime.datetime.strftime(ms_datetime, "%M:%S.%f")[:-4]
        elif 36000 < self.time_10ms:
            self.formatted_time = datetime.datetime.strftime(ms_datetime, "%H:%M:%S.%f")[:-4][1:]
        else:
            self.formatted_time = "?!"

        if self.ready > 0:
            screen.blit(self.big_font.render(self.formatted_time, True, (255, 0, 0) if self.ready < 20 else (0, 255, 0)),
                        (screen.get_size()[0] / 2 - self.big_font.size(self.formatted_time)[0] / 2 - 10,
                         screen.get_size()[1] / 2 - self.big_font.size(self.formatted_time)[1] / 2))
        else:
            screen.blit(self.big_font.render(self.formatted_time, True, (255, 255, 255)),
                        (screen.get_size()[0] / 2 - self.big_font.size(self.formatted_time)[0] / 2 - 10,
                         screen.get_size()[1] / 2 - self.big_font.size(self.formatted_time)[1] / 2))

        pygame.display.update()

    def draw_text(self, text, color, coords):
        self.screen.blit(self.font.render(text, True, color), coords)