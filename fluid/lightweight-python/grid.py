# to test the areas have 4 points

import pygame
import random
import math
 
pygame.init()


gravity = 9.81
damping = 0.99
debug = True


white = (255, 255, 255)
black = (0, 0, 0)
screen_height = 500
screen_width = 500

# inmit
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fluid")



class Point:
    def __init__(self, x, y, size):
        self.pos = [x*screen_width, y*screen_height]
        self.vector = [0,0]
    def update(self):
        # apply gravity to move points

        # get collisions to mark some points as unable to expand

        # calculate the size

        # compare to target size

        # expand as appropriate
        
        #self.draw()
        pass
    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255, 255), (self.pos[0], self.pos[1]), 2)
 
running = True
clock = pygame.time.Clock()

points = []
for i in range(10):
    for j in range(10):
        points.append(new Point( (i+1)*500/11 , (j+1)*500/11 ))

while running:
    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.WINDOWMOVED:
            pass # todo

    for p in points:
        a.draw()

    pygame.display.flip()
    clock.tick(60)
 
 
pygame.quit()
quit()
