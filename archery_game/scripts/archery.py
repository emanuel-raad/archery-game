from math import cos, sin

import pygame
from archery_game.engine.components import (CollisionComponent, CollisionType,
                                            CustomMotionComponent,
                                            NameComponent, PositionComponent,
                                            RenderComponent, ShooterComponent,
                                            VelocityComponent)
from archery_game.engine.ecs import Entity
from archery_game.engine.render import WHITE, RenderSystem
from archery_game.engine.systems import (CollisionSystem, CustomMotionSystem,
                                         PairedSystem, PhysicsSystem,
                                         ScoreSystem, ShooterSystem)


def main():
    pygame.init()
    pygame.display.set_caption("Arrow Game")

    width = 480
    height = 360
    size = (width, height)
    
    screen = pygame.display.set_mode(size, 0, 32)
    screen.fill(WHITE)

    # define a variable to control the main loop
    running = True

    floor = Entity([
        NameComponent("floor"),
        PositionComponent(),
        CollisionComponent(
            x1=0, x2=width, y1=20, y2=0,
            ctype=CollisionType.RIGID
        ),
        RenderComponent()
    ])

    target = Entity([
        NameComponent("target"),
        PositionComponent(250, 250),
        RenderComponent(),
        CollisionComponent(
            x1=245, x2=255, y1=270, y2=220,
            ctype=CollisionType.RIGID
        ),
        CustomMotionComponent(
            expression_y = lambda t : 80*sin(t)
        )
    ])

    bow = Entity([
        ShooterComponent(0.25, 1, 21, r = 30),
        RenderComponent()
    ])

    physics  = PhysicsSystem()
    renderer = RenderSystem()
    collider = CollisionSystem()
    pairer = PairedSystem()
    shooter = ShooterSystem()
    move = CustomMotionSystem()
    scorer = ScoreSystem()

    t = 0
    dt = 5 / 60

    speed = 70

    # main loop
    while running:
        screen.fill(WHITE)

        shooter.update()

        move.update(t)

        physics.update('y', dt = dt)
        collider.update('y')
        physics.update('x', dt = dt)
        collider.update('x')

        pairer.update()
        renderer.update(screen, width, height)
        scorer.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Entity([
                        NameComponent("arrow"),
                        PositionComponent(bow.shooter.x, bow.shooter.y),
                        VelocityComponent(speed*cos(bow.shooter.angle), speed*sin(bow.shooter.angle)),
                        RenderComponent(),
                        CollisionComponent(
                            x1=bow.shooter.x, x2=bow.shooter.x+1,
                            y1=bow.shooter.y, y2=bow.shooter.y-1,
                            ctype=CollisionType.STICK
                        ),
                    ])

        t += dt
        pygame.display.update()
        pygame.time.delay(int(1/60 * 1000))
          
if __name__=="__main__":
    main()