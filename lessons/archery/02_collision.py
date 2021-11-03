import time
from math import cos, sin

import pygame
from archery_game.engine.components import (CollisionComponent, CollisionType,
                                            NameComponent, PositionComponent,
                                            RenderComponent, VelocityComponent)
from archery_game.engine.ecs import Entity
from archery_game.engine.render import WHITE, RenderSystem
from archery_game.engine.systems import (CollisionSystem, PairedSystem,
                                         PhysicsSystem)


class MyCollisionSystem(CollisionSystem):
    r"""
        Find collisions
    """
    
    def __init__(self):
        super().__init__()

    @staticmethod
    def is_collision(e1 : Entity, e2 : Entity):
        # The entity objects have the following members:
        #   e.collide.x1 ( left side   )
        #   e.collide.x2 ( right side  )
        #   e.collide.y1 ( top side    )
        #   e.collide.y2 ( bottom side )
        # 
        # Return true if there is a collision, false otherwise
        return False


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
        RenderComponent()
    ])

    physics  = PhysicsSystem()
    collider = MyCollisionSystem()
    renderer = RenderSystem()
    pairer   = PairedSystem()

    t     = 0            # the initial time
    dt    = 5 / 60       # the simulator time step
    frame = 1/60 * 1000  # the length of time for one frame to run at 60 fps
    speed = 80           # the speed of the arrow

    angle = 75 * (3.14159 / 180)

    running = True
    while running:
        start = time.time()
        screen.fill(WHITE)

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
        elapsed = 1000 * (time.time() - start)
        delay = 0 if elapsed > frame else frame - elapsed
        pygame.time.delay(int(delay))
          
if __name__=="__main__":
    main()
