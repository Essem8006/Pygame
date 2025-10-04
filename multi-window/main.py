import threading
import pygame

pygame.init()
black = (0, 0, 0)
screen_dimention = 300
 
def window():
    pygame.init()
    screen = pygame.display.set_mode((screen_dimention, screen_dimention))
    pygame.draw.rect(screen, black, [0, 0, screen_dimention, screen_dimention])
    pygame.display.update()
    running=True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False

if __name__ =="__main__":
    t1 = threading.Thread(target=window,args=())
    t2 = threading.Thread(target=window,args=())
    t1.start()
    t2.start()
    t1.join()
    t2.join()

pygame.quit()
quit()
