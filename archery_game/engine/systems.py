from enum import unique
from itertools import combinations
from math import atan2, cos, sin
from typing import Callable, List

import pygame
from archery_game.engine.components import (CollisionComponent, CollisionType,
                                            CustomMotionComponent,
                                            NameComponent, PairedComponent,
                                            PositionComponent, RotateComponent,
                                            ShooterComponent,
                                            VelocityComponent)
from archery_game.engine.ecs import Entity, System


class RotateSystem(System):
    def __init__(self):
        super().__init__()

        self.subscribe(RotateComponent)
        self.subscribe(VelocityComponent)

    def update(self):
        entities = self.get()

        for e in entities:
            # mag = sqrt(e.velocity.vx**2 + e.velocity.vy**2)
            if e.rotate.rotateWithVelocity:
                e.rotate.ux = e.velocity.vx # / mag
                e.rotate.uy = e.velocity.vy # / mag
                e.rotate.ut = atan2(e.rotate.uy, e.rotate.ux)

class PhysicsSystem(System):
    def __init__(self):
        super().__init__()

        self.subscribe(PositionComponent)
        self.subscribe(VelocityComponent)

    def update(self, mode : str, dt : float = 0.01):
        entities = self.get()

        for e in entities:
            ax = 0.0
            ay = -9.81

            if mode == 'x':
                e.velocity.vx += ax * dt
                e.position.x += e.velocity.vx * dt
                if e.has(CollisionComponent):
                    e.collide.x1 += e.velocity.vx * dt
                    e.collide.x2 += e.velocity.vx * dt

            elif mode == 'y':
                e.velocity.vy += ay * dt
                e.position.y += e.velocity.vy * dt
                if e.has(CollisionComponent):
                    e.collide.y1 += e.velocity.vy * dt
                    e.collide.y2 += e.velocity.vy * dt

class TrackTrajectorySystem(System):
    def __init__(self, exclusive: List[str] = []):
        super().__init__()
        
        self.subscribe(PositionComponent)
        self.entities = {}
        self.exclusive = exclusive

    def update(self):
        entities = self.get()

        for e in entities:
            if (len(self.exclusive) > 0 and e.id in self.exclusive) or not self.exclusive:                    
                if e.id not in self.entities:
                    self.entities[e.id] = {'x' : [], 'y' : []}

                self.entities[e.id]['x'] += [ e.position.x ]
                self.entities[e.id]['y'] += [ e.position.y ]

class CollisionSystem(System):
    r"""
        Find collisions
    """
    
    def __init__(self):
        super().__init__()

        self.subscribe(CollisionComponent)

    @staticmethod
    def is_collision(e1 : Entity, e2 : Entity):
        return (e1.collide.x1 < e2.collide.x2) \
            and (e1.collide.x2 > e2.collide.x1) \
            and (e1.collide.y1 > e2.collide.y2) \
            and (e1.collide.y2 < e2.collide.y1)

    @staticmethod
    def is_collision_x(e1 : Entity, e2 : Entity):
        return (e1.collide.x1 < e2.collide.x2) \
            and (e1.collide.x2 > e2.collide.x1)

    @staticmethod
    def is_collision_y(e1 : Entity, e2 : Entity):
        return (e1.collide.y1 > e2.collide.y2) \
            and (e1.collide.y2 < e2.collide.y1)

    def update(self, mode : str, **kwargs):
        entities = self.get()

        if mode == 'x':
            for (e1, e2) in combinations(entities, 2):
                if self.is_collision(e1, e2):
                    collision_x_handler(e1.id, e2.id)
                    if not (e1.collide.ctype == e2.collide.ctype == CollisionType.SLIDE):
                        collision_x_handler(e2.id, e1.id)

        elif mode == 'y':
            for (e1, e2) in combinations(entities, 2):
                if self.is_collision(e1, e2):
                    collision_y_handler(e1.id, e2.id)
                    if not (e1.collide.ctype == e2.collide.ctype == CollisionType.SLIDE):
                        collision_y_handler(e2.id, e1.id)

class PairedSystem(System):
    def __init__(self):
        super().__init__()

        self.subscribe(PairedComponent)
        self.subscribe(PositionComponent)

    def update(self):
        entities = self.get()

        for e in entities:
            paired = Entity.get(e.pair.pair_id)

            if not hasattr(e.pair, 'x'):
                e.pair.x = paired.position.x - e.position.x
            if not hasattr(e.pair, 'y'):
                e.pair.y = paired.position.y - e.position.y

            # Can also remove the collision component
            # so that arrows don't collide with each other
            # after hitting the target

            if e.has(CollisionComponent):
                if not hasattr(e.pair, 'x1'):
                    e.pair.x1 = paired.position.x - e.collide.x1
                    e.pair.x2 = paired.position.x - e.collide.x2
                if not hasattr(e.pair, 'y1'):
                    e.pair.y1 = paired.position.y - e.collide.y1
                    e.pair.y2 = paired.position.y - e.collide.y2

            e.position.x = paired.position.x - e.pair.x
            e.position.y = paired.position.y - e.pair.y

            if e.has(CollisionComponent):
                e.collide.x1 = paired.position.x - e.pair.x1
                e.collide.x2 = paired.position.x - e.pair.x2
                e.collide.y1 = paired.position.y - e.pair.y1
                e.collide.y2 = paired.position.y - e.pair.y2

            if e.has(VelocityComponent) and e.has(RotateComponent):
                e.rotate.rotateWithVelocity = False
                # e.dettach(VelocityComponent)

def collision_x_handler(id1, id2):
    _e1 = Entity.get(id1)
    _e2 = Entity.get(id2)

    collisions = [[_e1, _e2]]

    # if (_e1.collide.ctype == CollisionType.RIGID) \
    #     or (_e2.collide.ctype == CollisionType.RIGID):
    #     collisions += [[_e2, _e1]]

    for (e1, e2) in collisions:
        if (e1.collide.ctype == CollisionType.SLIDE):
            if (e1.collide.x2 > e2.collide.x1) and (e1.collide.x1 < e2.collide.x1):     
                diff = e1.collide.x2 - e2.collide.x1
                if e1.has(PositionComponent): e1.position.x -= diff
                e1.collide.x1 -= diff
                e1.collide.x2 -= diff
                # if e1.has(VelocityComponent): e1.velocity.vx = -0.3 * abs(e1.velocity.vx)

            if (e1.collide.x1 < e2.collide.x2) and (e1.collide.x2 > e2.collide.x2):
                diff = e2.collide.x2 - e1.collide.x1
                if e1.has(PositionComponent): e1.position.x += diff
                e1.collide.x1 += diff
                e1.collide.x2 += diff
                # if e1.has(VelocityComponent): e1.velocity.vx = 0.3 * abs(e1.velocity.vx)

        if (e1.collide.ctype == CollisionType.STICK) and not e1.has(PairedComponent):
            e1.attach(PairedComponent(e2.id))

def collision_y_handler(id1, id2):
    _e1 = Entity.get(id1)
    _e2 = Entity.get(id2)

    collisions = [[_e1, _e2]]

    # if (_e1.collide.ctype == CollisionType.RIGID) \
    #     or (_e2.collide.ctype == CollisionType.RIGID):
    #     collisions += [[_e2, _e1]]

    for (e1, e2) in collisions:
        if (e1.collide.ctype == CollisionType.SLIDE):
            if (e1.collide.y1 > e2.collide.y2) and (e1.collide.y2 < e2.collide.y2):
                diff = e1.collide.y1 - e2.collide.y2
                if e1.has(PositionComponent): e1.position.y -= diff
                e1.collide.y1 -= diff
                e1.collide.y2 -= diff
            if (e1.collide.y2 < e2.collide.y1) and (e1.collide.y1 > e2.collide.y1):
                diff = e2.collide.y1 - e1.collide.y2
                if e1.has(PositionComponent): e1.position.y += diff
                e1.collide.y1 += diff
                e1.collide.y2 += diff
                if e1.has(VelocityComponent): e1.velocity.vy = 0

        if (e1.collide.ctype == CollisionType.STICK) and not e1.has(PairedComponent):
            e1.attach(PairedComponent(e2.id))

class DrawSystem(System):
    r"""
        Draw objects to the screen
    """
    pass

class CustomMotionSystem(System):
    r"""
        Moves an object based on a pre-determined path
        without any physical interactions
    """
    
    def __init__(self):
        super().__init__()
        
        self.subscribe(PositionComponent)
        self.subscribe(CustomMotionComponent)

    def update(self, t : float = 0):
        entities = self.get()

        for e in entities:

            if not hasattr(e.motion, 'ox'):
                e.motion.ox = e.position.x
                if e.has(CollisionComponent):
                    e.motion.ox1 = e.collide.x1
                    e.motion.ox2 = e.collide.x2
            if not hasattr(e.motion, 'oy'):
                e.motion.oy = e.position.y
                if e.has(CollisionComponent):
                    e.motion.oy1 = e.collide.y1
                    e.motion.oy2 = e.collide.y2

            if e.motion.expression_x is not None:
                e.position.x = e.motion.expression_x(t) + e.motion.ox
                if e.has(CollisionComponent):
                    e.collide.x1 = e.motion.expression_x(t) + e.motion.ox1
                    e.collide.x2 = e.motion.expression_x(t) + e.motion.ox2
            if e.motion.expression_y is not None:
                e.position.y = e.motion.expression_y(t) + e.motion.oy
                if e.has(CollisionComponent):
                    e.collide.y1 = e.motion.expression_y(t) + e.motion.oy1
                    e.collide.y2 = e.motion.expression_y(t) + e.motion.oy2

class ShooterSystem(System):
    def __init__(self):
        super().__init__()

        self.subscribe(ShooterComponent)

    def update(self):
        entities = self.get()

        for e in entities:

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                e.shooter.angle += 0.05
            if keys[pygame.K_RIGHT]:
                e.shooter.angle -= 0.05
            
            rx = e.shooter.r * cos(e.shooter.angle) + e.shooter.x
            ry = e.shooter.r * sin(e.shooter.angle) + e.shooter.y

            if not e.has(PositionComponent):
                e.attach(PositionComponent(rx, ry))
            else:
                e.position.x = rx
                e.position.y = ry

class ScoreSystem(System):
    def __init__(self):
        super().__init__()

        self.subscribe(PairedComponent)

    def update(self, screen, **kwargs):
        entities = self.get()
        score = 0

        for e in entities:
            p = Entity.get(e.pair.pair_id)
            
            if p.has(NameComponent):
                if p.name.name == "target":
                    score += 1

        font = pygame.font.Font(pygame.font.get_default_font(), 30)
        text = font.render("Score: {}".format(score), True, 'black')
        screen.blit(text, (0, 0))

def cartesian_to_screen(cart_x, cart_y, width, height):
    screen_x = cart_x
    screen_y = height - cart_y

    return screen_x, screen_y

if __name__ == '__main__':
    arrow = Entity([
        NameComponent("arrow"),
        PositionComponent(),
        VelocityComponent(5*0.707, 5*0.707),
        CollisionComponent(x1=0, x2=0.001, y1=0.001, y2=0)
    ])

    target = Entity([
        NameComponent("target"),
        PositionComponent(),
        CustomMotionComponent(
            expression_x = lambda t: sin(10*t),
            expression_y = lambda t: sin(t)
        )
    ])

    wall = Entity([
        NameComponent("wall"),
        CollisionComponent(
            x1=1.50, x2=1.55, y1=3.0, y2=0,
            ctype=CollisionType.RIGID
        )
    ])

    physics  = PhysicsSystem()
    motion   = CustomMotionSystem()
    draw     = TrackTrajectorySystem()

    t = 0
    dt = 1 / 60
    for _ in range(3 * 60):
        physics.update(dt = dt)
        motion.update(t = t)
        draw.update()

        t += dt

    import matplotlib.pyplot as plt

    fig, axs = plt.subplots(nrows=1, ncols=2)

    xs = draw.entities[arrow.id]['x']
    ys = draw.entities[arrow.id]['y']
    axs[0].scatter(xs, ys)
    axs[0].grid()

    xs = draw.entities[target.id]['x']
    ys = draw.entities[target.id]['y']
    axs[1].scatter(xs, ys)
    axs[1].grid()
    
    plt.show()
