import pygame
from pygame._sdl2.video import Window
import random
import math
from utils import *
import threading
# Thread that draws and a thread that calculates
 
pygame.init()


gravity = 9.81/60
damping = 0.99
big_n = 1000


white = (255, 255, 255)
black = (0, 0, 0)
grey = (50, 0, 50)
red = (255, 0, 0)
screen_height = 500
screen_width = 500
screen_pos = None


class Particle:
    def __init__(self, x, y):
        self.pos = [x*screen_width, y*screen_height]
        self.vel = [0,0]
    def update(self, offset):
        acceleration = [0,gravity]
        grad = gradient(particles, self.pos)
        for i in range(2):
            self.vel[i] *= damping
            self.vel[i] += acceleration[i] + grad[i]
            self.pos[i] +=self.vel[i] + offset[i]
            if self.pos[i] < 0:
                self.pos[i] *= -1
                self.vel[i] *= -1
            elif self.pos[i] > screen_height:
                self.pos[i] = 2 * screen_height - self.pos[i]
                self.vel[i] *= -1
 
running = True
clock = pygame.time.Clock()

particles = []
for i in range(big_n):
    particles.append(Particle(random.random(), random.random()))

# for drawing density
quality = 50
ratio = screen_height/quality

def drawLoop():
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Fluid")

    circle_surface = pygame.Surface((10, 10), pygame.SRCALPHA)
    pygame.draw.circle(circle_surface, (255, 255, 255, 255), (5, 5), 5)
    global running
    while running:
        #events
        window_offset = [0,0]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            """elif event.type == pygame.WINDOWMOVED:
                if screen_pos:
                        window_offset = [screen_pos[0] - event.x, screen_pos[1] - event.y]
                screen_pos = [event.x, event.y]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                particles.append(Particle(event.pos[0]/screen_width, event.pos[1]/screen_height))"""

        """quality = 50
        ratio = screen_height/quality
        for i in range(quality):
            for j in range(quality):
                pygame.draw.rect(screen, (0, min(max(math.floor(60*density(particles, (i+0.5)*ratio, (j+0.5)*ratio)), 0), 255), 0), [i*ratio, j*ratio, ratio, ratio])"""
        pygame.draw.rect(screen, black, [0, 0, screen_width, screen_height])

        for part in particles:
            pygame.draw.circle(screen, (255, 255, 255, 255), part.pos, 2)

        pygame.display.flip()

def updateLoop():
    global running
    while running:
        for part in particles:
            part.update([0,0])# IGNORING WINDOW OFFSET FOR NOW

drawThread = threading.Thread(target=drawLoop)
updateThread = threading.Thread(target=updateLoop)

drawThread.start()
updateThread.start()
drawThread.join()
updateThread.join()
 
pygame.quit()
quit()
