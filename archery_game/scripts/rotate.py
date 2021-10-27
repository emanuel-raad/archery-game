from math import cos, sin, atan2

import pygame
import time
from archery_game.engine.components import PositionComponent
from archery_game.engine.ecs import Entity
from archery_game.engine.render import WHITE, RenderSystem

def main():
    width  = 480
    height = 360
    size   = (width, height)

    pygame.init()
    pygame.display.set_caption("Arrow Game")    
    screen = pygame.display.set_mode(size, 0, 32)
    screen.fill(WHITE)

    t     = 0            # the initial time
    dt    = 1 / 60       # the simulator time step
    frame = 1/60 * 1000  # the length of time for one frame to run at 60 fps

    def rot_center(image, rect, angle):
            """rotate an image while keeping its center"""
            rot_image = pygame.transform.rotate(image, angle)
            rot_rect = rot_image.get_rect(center=rect.center)
            return rot_image, rot_rect

    def rotatePivoted(im, angle, pivot):
        # rotate the leg image around the pivot
        image = pygame.transform.rotate(im, angle)
        rect = image.get_rect()
        rect.center = pivot
        return image, rect

    running = True
    while running:
        start = time.time()
        screen.fill(WHITE)

        img = pygame.image.load("archery_game//scripts//arrow2.png")
        # angle = sin(t) * 180 / 3.14159
        angle = t
        # img = pygame.transform.rotate(img, angle)
        # img, rect = rot_center(img, img.get_rect(), angle)
        img, rect = rotatePivoted(img, angle, (150, 150))
        # rect = img.get_rect()
        
        # rect.x = 150
        # rect.y = 150

        # pygame.draw.rect(screen, (255, 0, 0), rect)
        screen.blit(img, rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        t += dt
        pygame.display.update()
        # elapsed = 1000 * (time.time() - start)
        # delay = 0 if elapsed > frame else frame - elapsed
        # pygame.time.delay(int(delay))
          
if __name__=="__main__":
    main()