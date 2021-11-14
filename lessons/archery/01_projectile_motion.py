import time
from math import cos, sin

import pygame
from archery_game.engine.components import (NameComponent, PositionComponent,
                                            RenderComponent, VelocityComponent)
from archery_game.engine.ecs import Entity
from archery_game.engine.render import WHITE, RenderSystem
from archery_game.engine.systems import PhysicsSystem


class MyPhysicsSystem(PhysicsSystem):
    def __init__(self):
        super().__init__()

    def update(self, mode : str, dt : float = 0.01):
        entities = self.get()

        for e in entities:
            # Each entity object has the following members:
            #     e.position.x
            #     e.position.y
            #     e.velocity.vx
            #     e.velocity.vy
            # And the change in time is:
            #     dt

            ax = 0.0
            ay = -9.81

            if mode == 'x':
                # Update the x position and velocity here
                e.velocity.x = 0 # Add missing equation here
                e.position.x = 0 # ^

            elif mode == 'y':
                # Update the y position and velocity here
                e.velocity.y = 0 # Add missing equation here
                e.position.y = 0 # ^


def main():
    width  = 480
    height = 360
    size   = (width, height)

    pygame.init()
    pygame.display.set_caption("Arrow Game")    
    screen = pygame.display.set_mode(size, 0, 32)
    screen.fill(WHITE)

    physics  = MyPhysicsSystem()
    renderer = RenderSystem()

    t     = 0            # the initial time
    dt    = 5 / 60       # the simulator time step
    frame = 60           # the target framerate
    speed = 80           # the speed of the arrow
    angle = 75 * (3.14159 / 180)
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(frame)
        screen.fill(WHITE)

        physics.update('y', dt = dt)
        physics.update('x', dt = dt)

        renderer.update(screen, width, height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 
                    Entity([
                        NameComponent("arrow"),
                        PositionComponent(0, 0),
                        VelocityComponent(speed * cos(angle), speed * sin(angle)),
                        RenderComponent(
                            debug = True
                        )
                    ])

        font = pygame.font.Font(pygame.font.get_default_font(), 20)
        text = font.render("Press SPACE to shoot!", True, 'black')
        screen.blit(text, (0, 0))

        t += dt
        pygame.display.update()
          
if __name__=="__main__":
    main()
