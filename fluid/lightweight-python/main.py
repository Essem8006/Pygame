# to test the areas have 4 points

import pygame
import random
import math
 
pygame.init()


gravity = 9.81
damping = 0.99


white = (255, 255, 255)
black = (0, 0, 0)
screen_height = 500
screen_width = 500

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fluid")


class Area:
    def __init__(self, x, y, size):
        self.pos = [x*screen_width, y*screen_height]
        self.target_size = size
        self.size = 2
        self.points = [
            [x*screen_width-1, y*screen_height],
            [x*screen_width+1, y*screen_height],
            [x*screen_width, y*screen_height-1],
            [x*screen_width, y*screen_height+1],
        ]
        # apply gravity to move points

        # get collisions to mark some points as unable to expand

        # calculate the size

        # compare to target size

        # expand as appropriate
        
        #self.draw()
    def draw(self):
        pass # todo
 
running = True
clock = pygame.time.Clock()

areas = []
areas.append(new Area(0.5,0.5,10))

while running:
    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.WINDOWMOVED:
            pass # todo

    for a in areas:
        a.update()

    pygame.display.flip()
    clock.tick(60)
 
 
pygame.quit()
quit()
