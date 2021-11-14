import time
from math import atan2, cos, sin

import pygame
import argparse
from archery_game.engine.components import (CollisionComponent, CollisionType,
                                            CustomMotionComponent,
                                            NameComponent, PositionComponent,
                                            RenderComponent, RotateComponent,
                                            ShooterComponent,
                                            VelocityComponent)
from archery_game.engine.ecs import Entity
from archery_game.engine.render import WHITE, RenderSystem, gradientRect
from archery_game.engine.systems import (CollisionSystem, CustomMotionSystem,
                                         PairedSystem, PhysicsSystem,
                                         RotateSystem, ScoreSystem,
                                         ShooterSystem)


def main():

    parser = argparse.ArgumentParser(description='Archery game!.')
    parser.add_argument('--debug', default=False, help='Render in debug mode')
    args = parser.parse_args()

    width  = 480
    height = 360
    size   = (width, height)

    pygame.init()
    pygame.display.set_caption("Arrow Game")    
    screen = pygame.display.set_mode(size, 0, 32)
    screen.fill(WHITE)

    floor = Entity([
        NameComponent("floor"),
        PositionComponent(),
        CollisionComponent(
            x1=0, x2=width, y1=20, y2=0,
            ctype=CollisionType.RIGID
        ),
        RenderComponent(
            path = 'lessons//archery//grass.png',
            center = (0, 35),
            size = (width, 35),
            debug=False,
            priority=-1
        )
    ])

    sky_box = pygame.Rect(((0,0,width,width)))
    color_box = gradientRect(sky_box, (230, 242, 255), (0, 153, 255))
    color_box = pygame.transform.rotate(color_box, 90)

    target = Entity([
        NameComponent("target"),
        PositionComponent(245, 270),
        RenderComponent(
            path = 'lessons//archery//target.png',
            center = (0, 0),
            debug = args.debug,
            priority=1
        ),
        CollisionComponent(
            x1=245, x2=255, y1=270, y2=220,
            ctype=CollisionType.RIGID
        ),
        CustomMotionComponent(
            # expression_x = lambda t : 80*cos(t/1.5),
            expression_y = lambda t : 80*sin(t/1.5)
        )
    ])

    bow = Entity([
        ShooterComponent(0.707, 1, 21, r = 100),
        RenderComponent(
            path = "lessons//archery//aim.png",
            size = (20, 20),
            center = (10, 10),
            debug = False,
            priority=1
        )
    ])

    positions = [(x*50, 20) for x in range(10)]
    for (x, y) in positions:
        Entity([
            PositionComponent(x, y),
            RenderComponent(
                path = 'lessons//archery//tree.png',
                center = (20, 60),
                debug = False,
            ),
        ])
    for (x, y) in positions:
        Entity([
            PositionComponent(x+25, y),
            RenderComponent(
                path = 'lessons//archery//tree.png',
                center = (20, 80),
                size = (40, 80),
                debug = False
            ),
        ])
    positions = [(x*150, 20) for x in range(3)]
    for (x, y) in positions:
        Entity([
            PositionComponent(x+25, y),
            RenderComponent(
                path = 'lessons//archery//tree.png',
                center = (30, 180),
                size = (60, 180),
                debug = False
            ),
        ])


    physics  = PhysicsSystem()
    renderer = RenderSystem()
    collider = CollisionSystem()
    pairer   = PairedSystem()
    shooter  = ShooterSystem()
    move     = CustomMotionSystem()
    scorer   = ScoreSystem()
    rotater  = RotateSystem()

    t     = 0            # the initial time
    dt    = 5 / 60       # the simulator time step
    frame = 60           # the target framerate
    speed = 80           # the speed of the arrow
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(frame)
        screen.fill(WHITE)
        screen.blit(color_box, sky_box)

        shooter.update()

        move.update(t)

        physics.update('y', dt = dt)
        collider.update('y')
        physics.update('x', dt = dt)
        collider.update('x')

        pairer.update()
        rotater.update()
        renderer.update(screen, width, height)
        scorer.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 

                    x = 60
                    y = 10
                    col_x = x*cos(bow.shooter.angle) - y*sin(bow.shooter.angle)
                    col_y = x*sin(bow.shooter.angle) + y*cos(bow.shooter.angle)

                    Entity([
                        NameComponent("arrow"),
                        PositionComponent(bow.shooter.x+col_x, bow.shooter.y+col_y),
                        VelocityComponent(speed*cos(bow.shooter.angle), speed*sin(bow.shooter.angle)),
                        RotateComponent(rotateWithVelocity=True),
                        RenderComponent(
                            path = 'lessons//archery//arrow.png',
                            size = (60, 20),
                            center = (60, 10),
                            debug = args.debug,
                            priority=1
                        ),
                        CollisionComponent(
                            x1=bow.shooter.x+col_x, x2=bow.shooter.x+1+col_x,
                            y1=bow.shooter.y+col_y, y2=bow.shooter.y-1+col_y,
                            ctype=CollisionType.STICK
                        ),
                    ])

        font = pygame.font.Font(pygame.font.get_default_font(), 10)
        text = font.render("Press SPACE to shoot!", True, 'black')
        screen.blit(text, (0, 30))
        font = pygame.font.Font(pygame.font.get_default_font(), 10)
        text = font.render("Press LEFT and RIGHT to aim", True, 'black')
        screen.blit(text, (0, 45))

        t += dt
        pygame.display.update()
          
if __name__=="__main__":
    main()
