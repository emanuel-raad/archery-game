from dataclasses import dataclass as component

@component
class VelocityComponent:
    vx : float = 0.0
    vy : float = 0.0

@component
class PositionComponent:
    px : float = 0.0
    py : float = 0.0

@component
class NameComponent:
    name : str = ''
    def __repr__(self) -> str:
        return self.name