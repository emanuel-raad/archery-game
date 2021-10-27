import pygame

from archery_game.engine.ecs import Entity, System
from archery_game.engine.components import PositionComponent, ControlComponent, CollisionComponent

class MovementSystem(System):
    def __init__(self, entity_id):
        super().__init__()

        self.entity_id = entity_id
        e = Entity.get(self.entity_id)

        assert e.has(PositionComponent)
        assert e.has(ControlComponent)

    def update(self, mode : str):
        e = Entity.get(self.entity_id)

        keys = pygame.key.get_pressed()
        speed = 1

        if mode == 'x':
            if keys[pygame.K_LEFT]:
                e.position.x -= speed
                if e.has(CollisionComponent):
                    e.collide.x1 -= speed
                    e.collide.x2 -= speed
            if keys[pygame.K_RIGHT]:
                e.position.x += speed
                if e.has(CollisionComponent):
                    e.collide.x1 += speed
                    e.collide.x2 += speed
        
        elif mode == 'y':
            if keys[pygame.K_UP]:
                e.position.y += speed
                if e.has(CollisionComponent):
                    e.collide.y1 += speed
                    e.collide.y2 += speed
            if keys[pygame.K_DOWN]:
                e.position.y -= speed
                if e.has(CollisionComponent):
                    e.collide.y1 -= speed
                    e.collide.y2 -= speed