# density is dodgy

import pygame
import random
import math
 
pygame.init()

def get_density_grad(x,y, i, check, tile):
    density = 0
    gradient = [0,0]
    this_count=0
    inds = [tile]
    hold = tile
    while hold>10:
        hold-=10
    left = right = False
    if hold > 0:
        left = True
        inds.append(tile-1)
    if hold < 9:
        right = True
        inds.append(tile+1)
    if tile > 9:
        inds.append(tile-10)
        if left:
            inds.append(tile-11)
        if right:
            inds.append(tile-9)
    if tile < 90:
        inds.append(tile+10)
        if left:
            inds.append(tile+9)
        if right:
            inds.append(tile+11)
    for ind in inds:
        for pos, vel, gra in particles[ind]:
            difx = x-pos[0]
            dify = y-pos[1]
            dist = math.sqrt(difx*difx+dify*dify)
            if dist<100 and this_count != i:
                density+= (dist-100)*(dist-100)/200
                calc = 0.005*dist*dist - dist + 50
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

gravity = 9.81/60
damping = 0.8
particles = [[] for _ in range(100)]#position, velocity, gradient
big_n = 200
for i in range(10):
    for j in range(10):
        particles[10*i+j].append(([random.random()*50+50*i, random.random()*50+50*j], [0, 0], [0,0]))
        particles[10*i+j].append(([random.random()*50+50*i, random.random()*50+50*j], [0, 0], [0,0]))

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
    for i in range(10):
        for j in range(10):
            pygame.draw.rect(screen, (0,min(get_density_grad(i*50,j*50,1000, False, i*10+j)[0],255),0), [i*50, j*50, 50, 50])
    count=0
    to_decrease_x = []
    to_increase_x = []
    to_decrease_y = []
    to_increase_y = []
    to_decrease_y_dx = []
    to_increase_y_dx = []
    to_decrease_y_ix = []
    to_increase_y_ix = []
    for index in range(100):
        for position, velocity, grad in particles[index]:
            position[0]+=velocity[0]
            position[1]+=velocity[1]
            #velocity[1]+= gravity
            accel = get_density_grad(position[0],position[1],count, True, index)[1]
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
            hold = index
            height = 0
            while hold>10:
                hold-=10
                height+=1
            if position[0]<50*hold:
                if position[0]<50*height:
                    to_decrease_y_dx.append((index, (position, velocity, grad)))
                elif position[0]>50*height+50:
                    to_increase_y_dx.append((index, (position, velocity, grad)))
                else:
                    to_decrease_x.append((index, (position, velocity, grad)))
            elif position[0]>50*hold+50:
                if position[0]<50*height:
                    to_decrease_y_ix.append((index, (position, velocity, grad)))
                elif position[0]>50*height+50:
                    to_increase_y_ix.append((index, (position, velocity, grad)))
                else:
                    to_increase_x.append((index, (position, velocity, grad)))
            elif position[0]<50*height:
                to_decrease_y.append((index, (position, velocity, grad)))
            elif position[0]>50*height+50:
                to_increase_y.append((index, (position, velocity, grad)))

    for inde, spec in to_decrease_x:
        particles[inde].remove(spec)
        particles[inde-1].append(spec)
    for inde, spec in to_increase_x:
        particles[inde].remove(spec)
        particles[inde+1].append(spec)
    for inde, spec in to_decrease_y:
        particles[inde].remove(spec)
        particles[inde-10].append(spec)
    for inde, spec in to_increase_y:
        particles[inde].remove(spec)
        particles[inde+10].append(spec)
    for inde, spec in to_decrease_y_dx:
        particles[inde].remove(spec)
        particles[inde-11].append(spec)
    for inde, spec in to_increase_y_dx:
        particles[inde].remove(spec)
        particles[inde+9].append(spec)
    for inde, spec in to_decrease_y_ix:
        particles[inde].remove(spec)
        particles[inde-9].append(spec)
    for inde, spec in to_increase_y_ix:
        particles[inde].remove(spec)
        particles[inde+11].append(spec)
    pygame.display.update()
    #clock.tick(60)
 
 
pygame.quit()
quit()
