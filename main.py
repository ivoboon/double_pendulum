import pygame
import math

pygame.init()

screen_width = 1000
screen_height = 1000

surface = pygame.display.set_mode((screen_width, screen_height))

l1 = 200
pivot = [500, 500]
theta1 = 0
l2 = 200
theta2 = 0

colour = [255, 255, 255]

run = True

while run:

    surface.fill((0, 0, 0))

    x1 = l1 * math.sin(theta1)
    y1 = -l1 * math.cos(theta1)

    x2 = x1 + l2 * math.sin(theta2)
    y2 = y1 - l2 * math.cos(theta2)

    xy1 = [pivot[0] + x1, pivot[1] + y1]
    xy2 = [pivot[0] + x2, pivot[1] + y2]

    pygame.draw.circle(surface, colour, pivot, 5, 0)
    pygame.draw.line(surface, colour, [pivot[0] - 100, pivot[1]], [pivot[0] + 100, pivot[1]], 1)

    pygame.draw.aaline(surface, colour, pivot, xy1)
    pygame.draw.circle(surface, colour, xy1, 10, 0)

    pygame.draw.aaline(surface, colour, xy1, xy2)
    pygame.draw.circle(surface, colour, xy2, 10, 0)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()

    theta1 += 0.001
    theta2 -= 0.001

pygame.quit