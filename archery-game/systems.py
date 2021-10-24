from ecs import System, Entity
from components import PositionComponent, VelocityComponent, NameComponent

class PhysicsSystem(System):
    def __init__(self):
        super().__init__()

        self.subscribe(PositionComponent)
        self.subscribe(VelocityComponent)

    def update(self):
        pass

if __name__ == '__main__':
    arrow = Entity([
        NameComponent("arrow"),
        VelocityComponent(),
        PositionComponent()
    ])

    target = Entity([
        NameComponent("target"),
        PositionComponent(),
    ])

    physics = PhysicsSystem()
    res = physics.get()

    for r in res:
        name = r.getC(NameComponent)
        if name is not None:
            print(name)
        else:
            print(r)