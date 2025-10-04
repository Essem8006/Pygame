import pygame
import math
import random
from utils import *
 
pygame.init()

mountain_cols = [
    (3, 59, 108),
    (120, 177, 162),
    (56, 128, 153),
    (27, 83, 120),
    (24, 106, 130),
    (27, 83, 120)
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
    day_top = (99, 207, 246)
    day_bottom = (160, 219, 235)
    sunset_top = (17, 21, 68)
    sunset_bottom = (158, 72, 97)
    night_top = (24, 5, 1)
    night_bottom = (19, 13, 52)
    y/=screen_dimention
    if y < 0.25:
        return gradient(day_top,day_bottom,segments)
    elif y > 0.75:
        return gradient(night_top,night_bottom,segments)
    else:
        diff = 1-abs(2*y-1)*2
        if y < 0.5:
            top = mixCol(day_top,sunset_top,diff)
            bottom = mixCol(day_bottom,sunset_bottom,diff)
            return gradient(top,bottom,segments)
        else:
            top = mixCol(night_top,sunset_top,diff)
            bottom = mixCol(night_bottom,sunset_bottom,diff)
            return gradient(top,bottom,segments)

def sunColGradient(y):
    col = [(254, 254, 223),
    (255, 251, 123),
    (255, 235, 53),
    (254, 207, 34),
    (253, 174, 53),
    (252, 132, 13),
    (255, 103, 15),
    (233, 70, 5)]
    y /=screen_dimention
    y *= 10
    y = min(y,7)
    lower = col[math.floor(y)]
    higher = col[math.ceil(y)]
    diff = y - math.floor(y)
    return mixCol(lower,higher,diff)

class Sun:
    def __init__(self):
        self.pos = (60,60)
        self.r = 30
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
        pygame.draw.polygon(screen,(223, 254, 254),newWaveHighlight(this_x,screen_dimention * 0.7+y_below_horizon))
class Wave:
    def __init__(self):
        self.update()
    def update(self):
        self.x = math.floor(random.random() * screen_dimention)
        self.y = math.floor((random.random() * 0.3 + 0.7) * screen_dimention + 2)
    def draw(self):
        pygame.draw.polygon(screen,(223, 254, 254),newWaveHighlight(self.x,self.y))
wave_highlights = []
for i in range(50):
    wave_highlights.append(WaveHighlight())
waves = []
for i in range(50):
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
    #draw sky
    count=0
    for i in range(settings['sky_segments']):
        pygame.draw.rect(screen, sun.sky_col[i], [0, math.floor(screen_dimention*count), screen_dimention, math.ceil(screen_dimention*sky_dist[i])])
        count+=sky_dist[i]
    sun.draw()
    pygame.draw.rect(screen, sea_col, [0, screen_dimention*0.7, screen_dimention, screen_dimention*0.3])
    if sun.pos[1] < screen_dimention*0.7:
        for wave in wave_highlights:
            wave.draw()
    for wave in waves:
        wave.draw()
    holder = getMountains(screen_dimention,screen_dimention*0.7)
    count = 0
    for section in holder:
        pygame.draw.polygon(screen, mountain_cols[count],section)
        count += 1
    pygame.display.update()
 
 
pygame.quit()
quit()
