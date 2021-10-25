from ecs import System, Entity
from components import \
    PositionComponent, VelocityComponent, NameComponent, CustomMotionComponent

from typing import List
from math import sin, cos

class PhysicsSystem(System):
    def __init__(self):
        super().__init__()

        self.subscribe(PositionComponent)
        self.subscribe(VelocityComponent)

    def update(self, dt : float = 0.01):
        entities = self.get()

        for e in entities:
            # Object out of bounds
            # Can also implement an out-of-bounds system
            # Not perfect but gets the job done
            e.position.x += e.velocity.vx * dt

            potential_y = e.velocity.vy * dt
            if (e.position.y + potential_y) < 0:
                e.position.y = 0
                e.velocity.vy = 0
                e.velocity.vx = 0
            else:
                e.position.y += potential_y

            ax = 0.0
            ay = -9.81

            e.velocity.vx += ax * dt
            e.velocity.vy += ay * dt

class DrawTrajectorySystem(System):
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
    pass

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
            if e.motion.expression_x is not None:
                e.position.x = e.motion.expression_x(t)
            if e.motion.expression_y is not None:
                e.position.y = e.motion.expression_y(t)

if __name__ == '__main__':
    arrow = Entity([
        NameComponent("arrow"),
        PositionComponent(),
        VelocityComponent(5*0.707, 5*0.707),
    ])

    target = Entity([
        NameComponent("target"),
        PositionComponent(),
        CustomMotionComponent(
            expression_x = lambda t: sin(10*t),
            expression_y = lambda t: sin(t)
        )
    ])

    physics = PhysicsSystem()
    motion  = CustomMotionSystem()
    draw    = DrawTrajectorySystem()

    t = 0
    dt = 1 / 60
    for _ in range(60):
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