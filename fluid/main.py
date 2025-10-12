# last working version

import pygame
import random
import math
 
pygame.init()


debug = False
gravity = 9.81/60
damping = 0.95
particles = []#position, velocity
big_n = 100

closeness_that_matters = 100


def get_density_grad(x,y, i, check):
    density = 0
    gradient = [0, 0]
    this_count = 0
    for pos, vel in particles:
        if this_count != i:
            difx = x - pos[0]
            dify = y - pos[1]
            dist = math.sqrt( difx * difx + dify * dify )
            if dist < closeness_that_matters:
                density += (dist - 100) * (dist - 100) / 200

                calc = (dist - 100) * (dist - 100) / 100 #0.005 * dist * dist - dist + 50
                calc_ang = math.atan2(pos[1]-y,pos[0]-x)
                gradient[0]-=math.cos(calc_ang)*calc
                gradient[1]-=math.sin(calc_ang)*calc
                if(check):
                    vel[0]+=math.cos(calc_ang)*calc/big_n
                    vel[1]+=math.sin(calc_ang)*calc/big_n
        this_count+=1
    return [density, gradient]
 
white = (255, 255, 255)
black = (0, 0, 0)
grey = (50, 0, 50)
red = (255, 0, 0)
screen_height = 500
screen_width = 500

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fluid")
 
running = True
clock = pygame.time.Clock()

for i in range(big_n):
    particles.append(([random.random()*screen_width, random.random()*screen_height], [0, 0]))

circle_surface = pygame.Surface((10, 10), pygame.SRCALPHA)
pygame.draw.circle(circle_surface, (255, 255, 255, 255), (5, 5), 5)

while running:
    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()

    pygame.draw.rect(screen, black, [0, 0, screen_width, screen_height])
    if debug:
        for i in range(10):
            for j in range(10):
                pygame.draw.rect(screen, (0,min(get_density_grad(i*50,j*50,1000, False)[0]*100/big_n,255),0), [i*50, j*50, 50, 50])
    count=0
    for position, velocity in particles:
        position[0]+=velocity[0]
        position[1]+=velocity[1]
        velocity[1]+= gravity
        accel = get_density_grad(position[0],position[1],count, False)[1]
        velocity[0]*=damping
        velocity[1]*=damping
        velocity[0]+=accel[0]/big_n
        velocity[1]+=accel[1]/big_n

        if position[1]>screen_height-10:
            velocity[1] = -velocity[1] * damping
            position[1] = screen_height-10
        elif position[1]<10:
            velocity[1] = -velocity[1] * damping
            position[1] = 10
        if position[0]>screen_width-10:
            velocity[0] = -velocity[0] * damping
            position[0] = screen_width-10
        elif position[0]<10:
            velocity[0] = -velocity[0] * damping
            position[0] = 10
        screen.blit(circle_surface, (position[0]-5, position[1]-5))
        count+=1

    pygame.display.update()
    #clock.tick(60)
 
 
pygame.quit()
quit()
