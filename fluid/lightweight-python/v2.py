import pygame
import random
import math
 
pygame.init()


gravity = 9.81
damping = 0.0125
debug = True
N = 30



width = 500/(2*(N+1))
line_scale = width - 1


white = (255, 255, 255)
black = (0, 0, 0)
screen_height = 500
screen_width = 500

# inmit
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fluid")

def cap_col(col):
    return max(min(col, 255), 0)


class Point:
    def __init__(self, x, y):
        self.value = random.random()
        self.velocity = [0,0,0,0]

        self.pos = [x*screen_width, y*screen_height]
        self.flow = [0,0,0,0]

    def update(self, surrounding):

        self.velocity[0] += 0.01# + window_offset[1] * 0.002   # down
        #self.velocity[2] +=       - window_offset[1] * 0.002   # up
        #self.velocity[1] +=       - window_offset[0] * 0.002   # right
        #self.velocity[3] +=         window_offset[0] * 0.002   # left

        for i in range(4):
            self.velocity[i] *= 0.95
            self.velocity[i] += max(self.value - surrounding[i], 0) * damping
            
            if surrounding[i] >= 1.0:
                self.flow[i] = 0.0  # cell is full, don't push in
            else:
                available = 1.0 - surrounding[i]
                self.flow[i] = min(self.velocity[i], self.value * 0.25, available)

        
        
        # error check
        if sum(self.flow) > self.value:
            #print(self.value)
            pass

        if self.value > 1:
            #print(self.value)
            pass

    def draw(self):
        if self.value > 0.5:
            color = (0, 0, 200)  # solid blue
        elif self.value > 0.1:
            color = (0, 0, int(200 * self.value * 2))  # partial
        else:
            color = black
        pygame.draw.rect(screen, color, [self.pos[0]-width, self.pos[1]-width, 2*width, 2*width])
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
    #screen_pos = get_window_position()
    #window_offset = [prev_window_pos[0] - screen_pos[0], 
    #                 prev_window_pos[1] - screen_pos[1]]
    #prev_window_pos = screen_pos
    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.WINDOWMOVED:
            print('_________')
            #if screen_pos:
            #        window_offset = [screen_pos[0] - event.x, screen_pos[1] - event.y]
            #screen_pos = [event.x, event.y]
    x, y = pygame.display.get_window_position()
    print(x, y)

    pygame.draw.rect(screen, black, [0, 0, 500, 500])

    # get flow
    for y in range(N):
        for x in range(N):
            up    = points[y-1][x].value if y > 0   else 1.0
            down  = points[y+1][x].value if y < N-1 else 1.0
            left  = points[y][x-1].value if x > 0   else 1.0
            right = points[y][x+1].value if x < N-1 else 1.0
            
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
