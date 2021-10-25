from dataclasses import dataclass as component
from typing import Callable
    
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

    # The normal vector that points perpendicular to
    # the direction of motion
    nx : float = 0.0
    ny : float = 0.0

@component
class NameComponent:
    namespace = 'name'

    name : str
    
    def __repr__(self) -> str:
        return self.name

@component
class CollisionComponent:
    # placeholder class
    pass

@component
class CustomMotionComponent:
    namespace = 'motion'

    expression_x : Callable[[float], float] = None
    expression_y : Callable[[float], float] = None