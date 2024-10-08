
import pygame
import random
import math
pi = math.pi
 
pygame.init()
 
white = (255, 255, 255)
black = (0, 0, 0)
grey = (50, 0, 50)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
screen_height = 500
screen_width = 500

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Agents")

#init
agents = []# x, y, theta
for i in range(10000):
    agents.append((20*math.cos(pi*i/5000)+screen_width/2,20*math.sin(pi*i/5000)+screen_height/2,pi*i/5000))
for i in range(50):
    agents.append((random.random()*screen_width,random.random()*screen_height, random.random()*2*pi))

running = True
 
while running:
    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()
    #logic
    rect_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    rect_surface.fill((0, 0, 0, 2))
    screen.blit(rect_surface, (0, 0))
    count = 0
    for x, y, theta in agents:
        try:
            node1 = screen.get_at( (round(x+math.cos(theta+1)*4),round(y+math.sin(theta+1)*4)) )[0]
        except:
            node1 = 0
        try:
            node2 = screen.get_at( (round(x+math.cos(theta)*4),round(y+math.sin(theta)*4)) )[0]
        except:
            node2 = 0
        try:
            node3 = screen.get_at( (round(x+math.cos(theta-1)*4),round(y+math.sin(theta-1)*4)) )[0]
        except:
            node3 = 0
        if node1>node2 and node1>node3:
            agents[count]= (x+math.cos(theta)/10,y+math.sin(theta)/10,theta+0.05)
        elif node3>node1 and node3>node2:
            agents[count]= (x+math.cos(theta)/10,y+math.sin(theta)/10,theta-0.05)
        else:
            agents[count]= (x+math.cos(theta)/10,y+math.sin(theta)/10,theta+random.random()/10-0.05)
        count+=1
        pygame.draw.rect(screen, white, [x, y, 1, 1])
    pygame.display.update()
 
pygame.quit()
quit()
