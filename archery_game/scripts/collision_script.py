import pygame
from math import sin, cos

from archery_game.engine.ecs import Entity
from archery_game.engine.components import \
    PositionComponent, CollisionComponent, RenderComponent, \
    NameComponent, ShooterComponent, VelocityComponent, CustomMotionComponent, \
    CollisionType, ControlComponent, PairedComponent
from archery_game.engine.render import WHITE, RenderSystem
from archery_game.engine.userinput import MovementSystem
from archery_game.engine.systems import \
    PhysicsSystem, CollisionSystem, collision_x_handler, PairedSystem, ShooterSystem

def main():
    pygame.init()
    pygame.display.set_caption("Collision Script")
    
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

    # wall = Entity([
    #     NameComponent("floor"),
    #     CollisionComponent(
    #         x1=0, x2=width, y1=150, y2=140,
    #         ctype=CollisionType.RIGID
    #     ),
    #     RenderComponent()
    # ])

    target = Entity([
        NameComponent("target"),
        PositionComponent(100, 100),
        CollisionComponent(
            x1=80, x2=120, y1=120, y2=80,
            ctype=CollisionType.RIGID
        ),
        ControlComponent(),
        RenderComponent()
    ])

    box = Entity([
        NameComponent("arrow"),
        PositionComponent(250, 250),
        VelocityComponent(0, 0),
        CollisionComponent(
            x1=220, x2=270, y1=270, y2=220,
            ctype=CollisionType.SLIDE
        ),
        RenderComponent(),
        # PairedComponent(target.id)
    ])

    bow = Entity([
        ShooterComponent(0.25, 1, 21, r = 30),
        RenderComponent()
    ])

    physics  = PhysicsSystem()
    renderer = RenderSystem()
    collider = CollisionSystem()
    # movement = MovementSystem(target.id)
    pairer = PairedSystem()
    shooter = ShooterSystem()

    t = 0
    dt = 1 / 60

    speed = 50

    # main loop
    while running:
        screen.fill(WHITE)

        # movement.update('y')
        physics.update('y', dt = dt)
        collider.update('y')

        # movement.update('x')
        physics.update('x', dt = dt)
        collider.update('x')

        shooter.update()

        pairer.update()

        renderer.update(screen, width, height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Entity([
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
        pygame.time.delay(int(dt * 1000))
          
if __name__=="__main__":
    main()