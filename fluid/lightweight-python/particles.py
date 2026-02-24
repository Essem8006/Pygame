
import pygame
import random
import math
 
pygame.init()


gravity = 9.81
damping = 0.0125
debug = True
N = 10



width = 500/(2*(N+1))
line_scale = width - 1


white = (255, 255, 255)
black = (0, 0, 0)
screen_height = 500
screen_width = 500

# inmit
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fluid")


class Point:
    def __init__(self, x, y):
        self.value = random.random()
        self.velocity = [0,0,0,0]

        self.pos = [x*screen_width, y*screen_height]
        self.flow = [0,0,0,0]

    def update(self, surrounding):
        for i in range(4):
            self.velocity[i] *= 0.95
            self.velocity[i] += max(self.value - surrounding[i], 0) * damping
            self.flow[i] = self.velocity[i]
        # error check
        if self.value > 1:
            print(self.value)

    def draw(self):
        pygame.draw.rect(screen, (0,255*self.value,0), [self.pos[0]-width, self.pos[1]-width, 2*width, 2*width])
        pygame.draw.circle(screen, white, (self.pos[0], self.pos[1]), 2)
        pygame.draw.line(screen, white, (self.pos[0], self.pos[1]), (self.pos[0], self.pos[1]+self.flow[0]*line_scale))
        pygame.draw.line(screen, white, (self.pos[0], self.pos[1]), (self.pos[0]+self.flow[1]*line_scale, self.pos[1]))
        pygame.draw.line(screen, white, (self.pos[0], self.pos[1]), (self.pos[0], self.pos[1]-self.flow[2]*line_scale))
        pygame.draw.line(screen, white, (self.pos[0], self.pos[1]), (self.pos[0]-self.flow[3]*line_scale, self.pos[1]))
 
running = True
clock = pygame.time.Clock()

points = []
for j in range(N):
    points.append([])
    for i in range(N):
        points[j].append(Point( (i+1)/(N+1), (j+1)/(N+1) ))

while running:
    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.WINDOWMOVED:
            pass # todo

    pygame.draw.rect(screen, black, [0, 0, 500, 500])

    # get flow
    for y in range(N):
        for x in range(N):
            if y == 0:
                up = points[y][x].value
                down = points[y+1][x].value
            elif y == N-1:
                up = points[y-1][x].value
                down = points[y][x].value
            else:
                up = points[y-1][x].value
                down = points[y+1][x].value
            
            if x == 0:
                left = points[y][x].value
                right = points[y][x+1].value
            elif x == N-1:
                left = points[y][x-1].value
                right = points[y][x].value
            else:
                left = points[y][x-1].value
                right = points[y][x+1].value
            
            surround = [down, right, up, left]
            points[y][x].update(surround)
            points[y][x].draw()

    # move water
    for y in range(N):
        for x in range(N):
            if y == 0:
                points[y+1][x].value += points[y][x].flow[0]
                points[y][x].value -= points[y][x].flow[0]
            elif y == N-1:
                points[y-1][x].value += points[y][x].flow[2]
                points[y][x].value -= points[y][x].flow[2]
            else:
                points[y+1][x].value += points[y][x].flow[0]
                points[y-1][x].value += points[y][x].flow[2]
                points[y][x].value -= points[y][x].flow[0]
                points[y][x].value -= points[y][x].flow[2]
            
            if x == 0:
                points[y][x+1].value += points[y][x].flow[1]
                points[y][x].value -= points[y][x].flow[1]
            elif x == N-1:
                points[y][x-1].value += points[y][x].flow[3]
                points[y][x].value -= points[y][x].flow[3]
            else:
                points[y][x+1].value += points[y][x].flow[1]
                points[y][x-1].value += points[y][x].flow[3]
                points[y][x].value -= points[y][x].flow[1]
                points[y][x].value -= points[y][x].flow[3]

    pygame.display.flip()
    clock.tick(60)
 
 
pygame.quit()
quit()
