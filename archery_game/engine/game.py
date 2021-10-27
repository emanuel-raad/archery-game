import pygame
from math import sin

from archery_game.engine.ecs import Entity
from archery_game.engine.components import PositionComponent, CollisionComponent, RenderComponent, \
    NameComponent, VelocityComponent, CustomMotionComponent, CollisionType
from archery_game.engine.render import WHITE, RenderSystem
from archery_game.engine.systems import PhysicsSystem, CustomMotionSystem, TrackTrajectorySystem
from archery_game.engine.systems import cartesian_to_screen

def main():
    pygame.init()
    pygame.display.set_caption("minimal program")
    
    width = 480
    height = 360
    size = (width, height)
    
    screen = pygame.display.set_mode(size, 0, 32)
    screen.fill(WHITE) 

    # define a variable to control the main loop
    running = True

    # box = Entity([
    #     PositionComponent(50, 50),
    #     CollisionComponent(x1=40, x2=60, y1=60, y2=40),
    #     RenderComponent()
    # ])

    arrow = Entity([
        NameComponent("arrow"),
        PositionComponent(),
        VelocityComponent(50*0.707, 50*0.707),
        CollisionComponent(x1=0, x2=10, y1=10, y2=0),
        RenderComponent()
    ])

    target = Entity([
        NameComponent("target"),
        PositionComponent(),
        CustomMotionComponent(
            expression_x = lambda t: 10*sin(10*t) + 50,
            expression_y = lambda t: 10*sin(t) + 50
        ),
        RenderComponent()
    ])

    wall = Entity([
        NameComponent("wall"),
        CollisionComponent(
            x1=50, x2=51, y1=60, y2=0,
            ctype=CollisionType.RIGID
        ),
        RenderComponent()
    ])

    physics  = PhysicsSystem()
    motion   = CustomMotionSystem()
    track    = TrackTrajectorySystem()
    renderer = RenderSystem()

    t = 0
    dt = 1 / 60

    # main loop
    while running:
        screen.fill(WHITE)

        physics.update(dt = dt)
        motion.update(t = t)
        track.update()
        renderer.update(screen, width, height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        t += dt
        pygame.display.update()
        pygame.time.delay(int(dt * 1000))
          
if __name__=="__main__":
    main()