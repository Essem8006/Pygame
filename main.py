#   Blit to surface not set_at
#   Downgrade the image quality first
#   Order by columns

import pygame
import math
from PIL import Image
pygame.init()
pi = math.pi
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
screen_height = 500
screen_width = 500

img = Image.open('earth/1200x600.jpeg')
img_data = img.getdata()
size = img.size

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Earth")
pygame.display.set_icon(pygame.image.load('earth/Earth.32.png'))
running = True

rotation = 0
widths = []
asins = []
for i in range(396):
    d = abs(198 - i)
    chord = 2*math.sqrt(198*198-d*d)
    widths.append(chord)
    asins.append(math.asin(i/198 - 1))

pygame.draw.rect(screen, black, [0, 0, screen_width, screen_height])
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #draw
    for this_x in range(396):
        this_ang = asins[this_x] - rotation
        if this_ang<0:
            this_ang+=2*pi
        img_index = round(size[0]*this_ang/(2*pi))
        for i in range(396):
            this_y = round(size[1]*(asins[i]/pi + 0.5))
            pygame.Surface.set_at(screen, (round(screen_width/2+(this_x-198)*widths[i]/396), round(screen_height*0.1+2+i)), img_data[size[0]*this_y+img_index])
    
    pygame.display.update()
    rotation+=0.01
    if rotation > 2*pi:
        rotation-=2*pi

pygame.quit()
quit()