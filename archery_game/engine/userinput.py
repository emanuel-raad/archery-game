import pygame

from archery_game.engine.ecs import Entity, System
from archery_game.engine.components import PositionComponent, ControlComponent, CollisionComponent

class MovementSystem(System):
    def __init__(self, entity_id, speed = 1, dir='xy'):
        super().__init__()

        self.entity_id = entity_id
        self.speed = speed
        self.dir = dir

        e = Entity.get(self.entity_id)

        assert e.has(PositionComponent)
        assert e.has(ControlComponent)

    def update(self, mode : str):
        e = Entity.get(self.entity_id)

        keys = pygame.key.get_pressed()
        speed = self.speed

        if mode == 'x' and 'x' in self.dir:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                e.position.x -= speed
                if e.has(CollisionComponent):
                    e.collide.x1 -= speed
                    e.collide.x2 -= speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                e.position.x += speed
                if e.has(CollisionComponent):
                    e.collide.x1 += speed
                    e.collide.x2 += speed
        
        elif mode == 'y' and 'y' in self.dir:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                e.position.y += speed
                if e.has(CollisionComponent):
                    e.collide.y1 += speed
                    e.collide.y2 += speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                e.position.y -= speed
                if e.has(CollisionComponent):
                    e.collide.y1 -= speed
                    e.collide.y2 -= speed