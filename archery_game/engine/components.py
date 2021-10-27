from dataclasses import dataclass as component
from enum import Enum
from typing import Callable

from archery_game.engine.ecs import Entity


@component
class PositionComponent:
    namespace = 'position'
    
    # The position vector components
    x : float = 0.0
    y : float = 0.0

@component
class VelocityComponent:
    namespace = 'velocity'

    # The velocity vector components
    vx : float = 0.0
    vy : float = 0.0

@component
class RotateComponent:
    namespace = 'rotate'

    # The right vector that points forward
    rx : float = 1.0
    ry : float = 0.0

    # The up vector that points up
    ux : float = 0.0
    uy : float = 1.0
    ut : float = 3.14159 / 2

    rotateWithVelocity : bool = False

@component
class NameComponent:
    namespace = 'name'

    name : str
    
    def __repr__(self) -> str:
        return self.name

class CollisionType(Enum):
    BOUNCE = 0
    SLIDE = 1
    RIGID = 2
    STICK = 3

@component
class CollisionComponent:
    namespace = 'collide'

    # Axis-aligned bounding box
    x1 : float # left
    x2 : float # right
    y1 : float # top
    y2 : float # bottom

    ctype : CollisionType = CollisionType.SLIDE

    def __post_init__(self):
        assert self.x1 < self.x2, 'CollisionComponent: x1 must be less than x2'
        assert self.y1 > self.y2, 'CollisionComponent: y1 must be greater than y2'

        self.height = self.y1 - self.y2
        self.width = self.x2 - self.x1
    
@component
class CustomMotionComponent:
    namespace = 'motion'

    expression_x : Callable[[float], float] = None
    expression_y : Callable[[float], float] = None

@component
class RenderComponent:
    namespace = 'render'

    path : str = None
    size : tuple = None
    center : tuple = None
    debug : str = True
    renderable : bool = True
    priority : int = 0

    def __lt__(self, other):
        return self.priority < other.priority

@component
class ControlComponent:
    namespace = 'control'
    
    controllable : bool = True

@component
class PairedComponent:
    namespace = 'pair'

    pair_id : int

    def __post_init__(self):
        assert Entity.get(self.pair_id).has(PositionComponent), \
            "PairedComponent: Paired entity must have a position component"

@component
class ShooterComponent:
    namespace = 'shooter'

    angle : float = 0
    x : float = 0
    y : float = 0
    r : float = 20
