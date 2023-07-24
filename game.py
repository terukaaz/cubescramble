import datetime
import json
import os
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

        self.auto_refresh = True

        self.load_config()
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
                        self.started = False # to stop the timer

                        fileutils.write_history(f"1.cth", self.formatted_time, self.current_scramble) # save

                        if self.auto_refresh:
                            self.refresh()

        if not self.started:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.ready += 1
            else:
                if self.ready >= 18: # start the timer
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

        self.formatted_time = self.format_time(self.time_10ms)

        if self.ready > 0:
            screen.blit(self.big_font.render(self.formatted_time, True, (255, 0, 0) if self.ready < 20 else (0, 255, 0)),
                        (screen.get_size()[0] / 2 - self.big_font.size(self.formatted_time)[0] / 2 - 10,
                         screen.get_size()[1] / 2 - self.big_font.size(self.formatted_time)[1] / 2))
        else:

            if self.started:

                display_time = self.format_time_custom(self.time_10ms)

                screen.blit(self.big_font.render(display_time, True, (255, 255, 255)),
                            (screen.get_size()[0] / 2 - self.big_font.size(display_time)[0] / 2 - 10,
                             screen.get_size()[1] / 2 - self.big_font.size(display_time)[1] / 2))
            else:

                screen.blit(
                    self.big_font.render(self.formatted_time, True, (255, 255, 255)),
                    (screen.get_size()[0] / 2 - self.big_font.size(self.formatted_time)[0] / 2 - 10,
                     screen.get_size()[1] / 2 - self.big_font.size(self.formatted_time)[1] / 2))

        pygame.display.update()

    def draw_text(self, text, color, coords):
        self.screen.blit(self.font.render(text, True, color), coords)

    def format_time(self, time_10ms):
        ms_datetime = datetime.datetime.fromtimestamp(time_10ms / 100.0) - datetime.timedelta(hours=1)  # very weird

        if time_10ms < 1000:
            formatted_time = datetime.datetime.strftime(ms_datetime, "%S.%f")[:-4][1:]
        elif 1000 < time_10ms < 6000:
            formatted_time = datetime.datetime.strftime(ms_datetime, "%S.%f")[:-4]
        elif 6000 < time_10ms < 60000:
            formatted_time = datetime.datetime.strftime(ms_datetime, "%M:%S.%f")[:-4][1:]
        elif 60000 < time_10ms < 360000:
            formatted_time = datetime.datetime.strftime(ms_datetime, "%M:%S.%f")[:-4]
        elif 36000 < time_10ms:
            formatted_time = datetime.datetime.strftime(ms_datetime, "%H:%M:%S.%f")[:-4][1:]
        else:
            formatted_time = "?!"

        return formatted_time

    def format_time_custom(self, time_10ms):
        ms_datetime = datetime.datetime.fromtimestamp(time_10ms / 100.0) - datetime.timedelta(hours=1)

        if time_10ms < 1000:
            formatted_time = datetime.datetime.strftime(ms_datetime, "%S")[1:]
        elif 1000 < time_10ms < 6000:
            formatted_time = datetime.datetime.strftime(ms_datetime, "%S")
        elif 6000 < time_10ms < 60000:
            formatted_time = datetime.datetime.strftime(ms_datetime, "%M:%S")[1:]
        elif 60000 < time_10ms < 360000:
            formatted_time = datetime.datetime.strftime(ms_datetime, "%M:%S")
        elif 36000 < time_10ms:
            formatted_time = datetime.datetime.strftime(ms_datetime, "%H:%M:%S")[1:]
        else:
            formatted_time = "?!"

        return formatted_time

    def save_config(self):

        filename = "config.json"

        with open(filename, 'w') as file:
            json.dump({
                "config": {
                    "puzzle": self.current_puzzle,
                    "auto_refresh": self.auto_refresh
                }
            }, file)

    def load_config(self):

        filename = "config.json"

        if filename not in os.listdir('.'):
            with open(filename, 'w') as file:
                json.dump({
                    "config": {
                        "puzzle": self.current_puzzle,
                        "auto_refresh": self.auto_refresh
                    }
                }, file)
                return

        with open(filename, "r") as file:
            try:
                data: dict = json.load(file)

                self.current_puzzle = data["config"]["puzzle"]
                self.auto_refresh = data["config"]["auto_refresh"]

            except json.decoder.JSONDecodeError as e:
                print(repr(e))