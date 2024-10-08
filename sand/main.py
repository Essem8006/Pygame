
import pygame
import random
 
pygame.init()
 
white = (255, 255, 255)
black = (0, 0, 0)
screen_dimention = 500

sand = []
sandsolid = [0] * screen_dimention

screen = pygame.display.set_mode((screen_dimention, screen_dimention))
pygame.display.set_caption("Sand")
 
running = True
 
while running:
    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            sand.append(event.pos)
            sand.append(event.pos)
            sand.append(event.pos)
            sand.append(event.pos)
    #fall
    count = 0
    tosolid = []
    togo = []
    for x, y in sand:
        if (x, y+1) not in sand and y+1<screen_dimention-sandsolid[x]:
            sand[count] = (x, y+1)
        elif y+1==screen_dimention-sandsolid[x]:
            sandsolid[x]+=1
            tosolid.append(count)
        count+=1
        if y>screen_dimention-sandsolid[x]:
            togo.append((x,y))

    tosolid.sort(reverse=True)
    for i in tosolid:
        sand.remove(sand[i])
    for x, y in togo:
        try:
            sand.remove((x,y))
        except:
            continue
    #roll
    for i in range(screen_dimention):
        left=False
        right=False
        if i > 0:
            if sandsolid[i]-1>sandsolid[i-1]:
                left = True
        if i < 499:
            if sandsolid[i]-1>sandsolid[i+1]:
                right = True
        if left and not right:
            sand.append((i-1,screen_dimention-sandsolid[i]))
            sandsolid[i]-=1
        elif right and not left:
            sand.append((i+1,screen_dimention-sandsolid[i]))
            sandsolid[i]-=1
        elif right and left:
            if random.random()>0.5:
                sand.append((i+1,screen_dimention-sandsolid[i]))
                sandsolid[i]-=1
            else:
                sand.append((i-1,screen_dimention-sandsolid[i]))
                sandsolid[i]-=1

    #draw
    pygame.draw.rect(screen, black, [0, 0, screen_dimention, screen_dimention])
    for x, y in sand:
        pygame.draw.rect(screen, white, [x, y, 1, 1])
    count=0
    for n in sandsolid:
        pygame.draw.rect(screen, white, [count, screen_dimention-n, 1, n+1])
        count+=1
    pygame.display.update()
 
 
pygame.quit()
quit()
