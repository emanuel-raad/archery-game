import time
from math import cos, sin

import pygame
from archery_game.engine.components import (CollisionComponent, CollisionType,
                                            NameComponent, PositionComponent,
                                            RenderComponent, VelocityComponent, CustomMotionComponent)
from archery_game.engine.ecs import Entity
from archery_game.engine.render import WHITE, RenderSystem
from archery_game.engine.systems import (CollisionSystem, CustomMotionSystem, PairedSystem,
                                         PhysicsSystem, CustomMotionComponent)


def x_movement(t : float) -> float:
    # If you don't want any x motion, then just return 0
    return 0.0

def y_movement(t : float) -> float:
    # If you don't want any y motion, then just return 0
    return 0.0


def main():
    width  = 480
    height = 360
    size   = (width, height)

    pygame.init()
    pygame.display.set_caption("Arrow Game")    
    screen = pygame.display.set_mode(size, 0, 32)
    screen.fill(WHITE)

    target = Entity([
        PositionComponent(300, 100),
        CollisionComponent(290, 310, 130, 70, ctype=CollisionType.RIGID),
        CustomMotionComponent(
            expression_x = x_movement,
            expression_y = y_movement
        ),
        RenderComponent()
    ])

    physics  = PhysicsSystem()
    collider = CollisionSystem()
    renderer = RenderSystem()
    pairer   = PairedSystem()
    mover    = CustomMotionSystem()

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

        mover.update(t)

        physics.update('y', dt = dt)
        collider.update('y')
        physics.update('x', dt = dt)
        collider.update('x')

        pairer.update()

        renderer.update(screen, width, height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 
                    Entity([
                        NameComponent("arrow"),
                        PositionComponent(0, 0),
                        CollisionComponent(0, 1, 1, 0, ctype=CollisionType.STICK),
                        VelocityComponent(speed * cos(angle), speed * sin(angle)),
                        RenderComponent(
                            debug = True
                        )
                    ])

        t += dt
        pygame.display.update()
          
if __name__=="__main__":
    main()
