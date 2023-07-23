import pygame

from scramblegenerator import clock

class Game:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.run = True

        self.font = pygame.font.Font("font.ttf", 25)
        self.current_scramble = ""
        self.current_puzzle = "clock"


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

                if event.key == pygame.K_SPACE:
                    self.refresh()

    def draw(self):

        screen = self.screen
        screen.fill((0, 0, 0))

        self.draw_text(self.current_scramble, (255, 255, 255), (10, 10))
        pygame.display.update()

    def draw_text(self, text, color, coords):
        self.screen.blit(self.font.render(text, True, color), coords)