import pygame

class Game:

    def __init__(self):
        self.run = True
        self.current_scramble = ""


    def refresh(self):
        pass

    def update(self):

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.refresh()

    def draw(self):
        pass