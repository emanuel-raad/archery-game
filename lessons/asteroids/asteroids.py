import random
import time
import uuid
from math import cos, sin

import pygame
from archery_game.engine.components import (AccelerationComponent,
                                            CollisionComponent, CollisionType,
                                            ControlComponent, NameComponent,
                                            PositionComponent, RenderComponent,
                                            RotateComponent, VelocityComponent)
from archery_game.engine.ecs import Entity, Observer, System
from archery_game.engine.render import WHITE, RenderSystem
from archery_game.engine.systems import CollisionSystem, PhysicsSystem
from archery_game.engine.userinput import MovementSystem


def asteroid_factory(x, y, vel, size=[20, 20]):
    offset = random.randint(-5, 5)
    sx = size[0] + offset
    sy = size[1] + offset
    s = (sx, sy)

    angle = random.randint(0, 360) * 3.14159 / 180

    return Entity([
        NameComponent( 'asteroid_' + str(uuid.uuid4()) ),
        PositionComponent(x, y),
        VelocityComponent(-vel, 0),
        AccelerationComponent(ay=0.0),
        RenderComponent(
            path = 'lessons/asteroids/asteroid.png',
            size = (2*s[0], 2*s[1]),
            center = (0, 0),
            debug = False,
        ),
        RotateComponent(ut = angle, rotateWithVelocity=False),
        CollisionComponent(
            ctype=CollisionType.RIGID,
            x1=x-s[0], x2=x+s[0], y1=y+s[0], y2=y-s[0]
        ),
    ])

def asteroid_spawner(framesSinceLastSpawn, lastSpawnX, width = 480, height=360):
    if framesSinceLastSpawn == 0:
        currentAsteroid = random.randint(0, height)
        while (abs(lastSpawnX - currentAsteroid) < 30):
            currentAsteroid = random.randint(0, height)

        asteroid_factory(width, currentAsteroid, 25)
        lastSpawnX = currentAsteroid

    return lastSpawnX

class GameState(Observer):
    def __init__(self):
        super().__init__()
        self.lose = False

        def _collision_callback(e1, e2, mode):
            names = ''
            if e1.has(NameComponent): names += e1.name.name
            if e2.has(NameComponent): names += e2.name.name

            if 'rocket' in names and 'asteroid' in names:
                print('you lose!')
                self.lose = True

        self.watch('collision', _collision_callback)

class AsteroidScoreSystem(System):
    def __init__(self):
        super().__init__()

        self.score = 0

        self.subscribe(PositionComponent)
        self.subscribe(NameComponent)

    def update(self, screen, **kwargs):
        entities = self.get()
    
        self.score = 0
        for e in entities:            
            if e.position.x < 0 and 'asteroid' in e.name.name:
                self.score += 1

        font = pygame.font.Font(pygame.font.get_default_font(), 30)
        text = font.render("Score: {}".format(self.score), True, 'white')
        screen.blit(text, (0, 0))

def main():
    width  = 480
    height = 360
    size   = (width, height)

    pygame.init()
    pygame.display.set_caption("Arrow Game")    
    screen = pygame.display.set_mode(size, 0, 32)
    screen.fill(WHITE)

    rocket = Entity([
        NameComponent("rocket"),
        PositionComponent(50, 50),
        ControlComponent(),
        RenderComponent(
            debug = False,
            path='lessons/asteroids/rocket.png',
            center=(20, 10)
        ),
        CollisionComponent(x1=30, x2=70, y1=60, y2=40)
    ])

    # Add some walls to the scene so the rocket can't cheat out
    Entity([ CollisionComponent(ctype=CollisionType.RIGID, x1=0, x2=width, y1=0, y2=-10) ])
    Entity([ CollisionComponent(ctype=CollisionType.RIGID, x1=0, x2=width, y1=height+10, y2=height) ])
    Entity([ CollisionComponent(ctype=CollisionType.RIGID, x1=-10, x2=0, y1=height, y2=0) ])
    Entity([ CollisionComponent(ctype=CollisionType.RIGID, x1=width, x2=width+10, y1=height, y2=0) ])

    # Add the skybox
    Entity([
        NameComponent('sky'),
        PositionComponent(0, height),
        RenderComponent(
            path = 'lessons/asteroids/skybox.png',
            priority = -1,
            debug=False
    )])

    mover    = MovementSystem(rocket.id, dir='xy', speed=3)
    physics  = PhysicsSystem()
    renderer = RenderSystem()
    collider = CollisionSystem()
    scorer   = AsteroidScoreSystem()

    game = GameState()

    t     = 0            # the initial time
    dt    = 5 / 60       # the simulator time step
    frame = 1/60 * 1000  # the length of time for one frame to run at 60 fps

    lastAsteroid = height/2

    counter = 0
    reset = 50

    running = True
    while running:
        start = time.time()
        screen.fill(WHITE)

        if not game.lose:
            # Asteroid spawning logic
            lastAsteroid = asteroid_spawner(counter, lastAsteroid)
            counter += 1
            if counter > reset:
                counter = 0

            # System updates
            mover.update('y')
            physics.update('y', dt = dt)
            collider.update('y')
            
            mover.update('x')
            physics.update('x', dt = dt)
            collider.update('x')

        # Rendering stage
        renderer.update(screen, width, height)
        scorer.update(screen=screen)
        if game.lose:
            font = pygame.font.Font(pygame.font.get_default_font(), 50)
            text = font.render("GAME OVER!", True, 'red')
            screen.blit(text, (width/6, height/2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        t += dt
        pygame.display.update()
        elapsed = 1000 * (time.time() - start)
        delay = 0 if elapsed > frame else frame - elapsed
        pygame.time.delay(int(delay))
          
if __name__=="__main__":
    main()