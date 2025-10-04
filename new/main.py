import pygame
import math
import random
from utils import *
 
pygame.init()

mountain_cols = [
    (23, 64, 96),#(3, 59, 108),
    (98, 98, 105),#(120, 177, 162),
    (105, 103, 106),#(56, 128, 153),
    (53, 85, 111),#(27, 83, 120),
    (82, 98, 110),#(24, 106, 130),
    (53, 85, 111)#(27, 83, 120)
]
sea_col = (150, 200, 255)
settings = {'sky_segments': 8}# higher means more light
sky_dist = []
for i in range(settings['sky_segments']):
    sky_dist.append(random.random())
sky_sum = sum(sky_dist)
for i in range(settings['sky_segments']):
    sky_dist[i] *= 0.7/sky_sum
screen_dimention = 500

screen = pygame.display.set_mode((screen_dimention, screen_dimention))
pygame.display.set_caption("Sun")

def skyColGradient(y):
    segments = settings['sky_segments']
    y/=screen_dimention

    grad = [
        ((99, 207, 246), (160, 219, 235), 0.35),#day
        ((187, 61, 55), (254, 149, 46), 0.58),#sunset
        ((17, 21, 68), (158, 72, 97), 0.67),#last light
        ((24, 5, 1), (19, 13, 52), 0.8)#night
    ]
    return changingGradient(grad,y,segments)

def sunColGradient(y):
    col = [(254, 254, 223),
    (255, 221, 131),
    (255, 221, 131)]
    y /=screen_dimention
    y *= 2
    lower = col[math.floor(y)]
    higher = col[math.ceil(y)]
    diff = y - math.floor(y)
    return mixCol(lower,higher,diff)

class Sun:
    def __init__(self):
        self.pos = (60,60)
        self.r = 179*250/1023
        self.col = (254, 254, 223)
        self.sky_col = skyColGradient(self.pos[1])
    def update(self, pos):
        self.pos = pos
        self.col = sunColGradient(self.pos[1])
        self.sky_col = skyColGradient(self.pos[1])
    def draw(self):
        pygame.draw.circle(screen, self.col, self.pos, self.r)

sun = Sun()

def newWaveHighlight(x,y):
    half_width = 10
    half_height = 2
    points = []
    points.append((x+half_width,y))
    points.append((x,y-half_height))
    points.append((x-half_width,y))
    points.append((x,y+half_height))
    return points
        
class WaveHighlight:
    def __init__(self):
        self.height_scale = random.random()
        self.x_offset = random.random()-0.5
    def update(self):
        self.height_scale = random.random()
        self.x_offset = random.random()-0.5
    def draw(self):
        height_above_horizon = screen_dimention * 0.7 - sun.pos[1]
        y_below_horizon = math.floor(self.height_scale * height_above_horizon)
        this_x = sun.pos[0] + self.x_offset * (height_above_horizon - y_below_horizon)
        pygame.draw.polygon(screen,mixCol((223, 254, 254),sun.col,0.5),newWaveHighlight(this_x,screen_dimention * 0.7+y_below_horizon))
class Wave:
    def __init__(self):
        self.update()
    def update(self):
        self.x = math.floor(random.random() * screen_dimention)
        self.y = math.floor((random.random() * 0.3 + 0.7) * screen_dimention + 2)
    def draw(self):
        pygame.draw.polygon(screen,lighter(sea_col,0.1),newWaveHighlight(self.x,self.y))
wave_highlights = []
for i in range(50):
    wave_highlights.append(WaveHighlight())
waves = []
for i in range(100):
    waves.append(Wave())

running = True
 
while running:
    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            sun.update(event.pos)
    #wave highlights
    if random.random() < 0.02:
        wave_highlights[math.floor(random.random()*len(wave_highlights))].update()
        waves[math.floor(random.random()*len(wave_highlights))].update()
    #draw sky
    count=0
    for i in range(settings['sky_segments']):
        pygame.draw.rect(screen, sun.sky_col[i], [0, math.floor(screen_dimention*count), screen_dimention, math.ceil(screen_dimention*sky_dist[i])])
        count+=sky_dist[i]
    #draw sun
    sun.draw()
    # draw sea
    sea_col = [0,0,0]
    for col in sun.sky_col:
        for i in range(3):
            sea_col[i] += col[i]
    for i in range(3):
        sea_col[i] /= len(sun.sky_col)
    sea_col[0] = max(0,sea_col[0]-30)
    sea_col[1] = max(0,sea_col[1]-30)
    sea_col[2] = min(255,sea_col[2]+30)
    pygame.draw.rect(screen, sea_col, [0, screen_dimention*0.7, screen_dimention, screen_dimention*0.3])
    if sun.pos[1] < screen_dimention*0.7:
        for wave in wave_highlights:
            wave.draw()
    for wave in waves:
        wave.draw()
    #draw mountains
    holder = getMountains(screen_dimention,screen_dimention*0.7)
    count = 0
    for section in holder:
        elevation = sun.pos[1]/screen_dimention
        if elevation > 0.8:
            shadow = 0.9
        elif elevation > 0.6:
            shadow = (sun.pos[1]/screen_dimention - 0.6) * 9/2
        else:
            shadow = 0
        pygame.draw.polygon(screen, lighter(mountain_cols[count],-1*shadow),section)
        count += 1

    pygame.display.update()

pygame.quit()
quit()
