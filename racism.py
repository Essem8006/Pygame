
import pygame
import random
import math
pi = math.pi
 
pygame.init()
 
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
screen_height = 700
screen_width = 1200

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Agents")

#init
agents = []# x, y, theta
agents2 = []# x, y, theta
for i in range(10000):
    agents.append((20*math.cos(pi*i/5000)+screen_width/2,20*math.sin(pi*i/5000)+screen_height/2,pi*i/5000))
for i in range(5000):
    #agents.append((random.random()*screen_width,random.random()*screen_height, random.random()*2*pi))
    agents2.append((random.random()*screen_width,random.random()*screen_height, random.random()*2*pi))

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
            hold = screen.get_at( (round(x+math.cos(theta+1)*4),round(y+math.sin(theta+1)*4)) )
            node1 = hold[0] - 2*hold[1]
        except:
            node1 = 0
        try:
            hold = screen.get_at( (round(x+math.cos(theta)*4),round(y+math.sin(theta)*4)) )
            node2 = hold[0] - 2*hold[1]
        except:
            node2 = 0
        try:
            hold = screen.get_at( (round(x+math.cos(theta-1)*4),round(y+math.sin(theta-1)*4)) )
            node3 = hold[0] - 2*hold[1]
        except:
            node3 = 0
        if node1>node2 and node1>node3:
            agents[count]= (x+math.cos(theta)/10,y+math.sin(theta)/10,theta+0.05)
        elif node3>node1 and node3>node2:
            agents[count]= (x+math.cos(theta)/10,y+math.sin(theta)/10,theta-0.05)
        else:
            agents[count]= (x+math.cos(theta)/10,y+math.sin(theta)/10,theta+random.random()/10-0.05)
        count+=1
        pygame.draw.rect(screen, red, [x, y, 1, 1])
    count = 0
    for x, y, theta in agents2:
        try:
            hold = screen.get_at( (round(x+math.cos(theta+1)*4),round(y+math.sin(theta+1)*4)) )
            node1 = hold[1] - 2*hold[0]
        except:
            node1 = 0
        try:
            hold = screen.get_at( (round(x+math.cos(theta)*4),round(y+math.sin(theta)*4)) )
            node2 = hold[1] - 2*hold[0]
        except:
            node2 = 0
        try:
            hold = screen.get_at( (round(x+math.cos(theta-1)*4),round(y+math.sin(theta-1)*4)) )
            node3 = hold[1] - 2*hold[0]
        except:
            node3 = 0
        if node1>node2 and node1>node3:
            agents2[count]= (x+math.cos(theta)/10,y+math.sin(theta)/10,theta+0.05)
        elif node3>node1 and node3>node2:
            agents2[count]= (x+math.cos(theta)/10,y+math.sin(theta)/10,theta-0.05)
        else:
            agents2[count]= (x+math.cos(theta)/10,y+math.sin(theta)/10,theta+random.random()/10-0.05)
        count+=1
        pygame.draw.rect(screen, green, [x, y, 1, 1])
    pygame.display.update()
 
pygame.quit()
quit()