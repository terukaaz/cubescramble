import pygame
import game

pygame.init()

clock = pygame.time.Clock()

size = (0, 0)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
size = screen.get_size()

game = game.Game()
run = True

while run:

    run = game.run

    clock.tick(60)
    game.draw()
    game.update()

pygame.quit()