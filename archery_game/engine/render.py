import pygame

from archery_game.engine.ecs import System
from archery_game.engine.components import PositionComponent, CollisionComponent, RenderComponent
from archery_game.engine.systems import cartesian_to_screen

WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255, 0, 0)

class RenderSystem(System):
    def __init__(self):
        super().__init__()

        self.subscribe(RenderComponent)

    def update(self, screen, width, height):
        entities = self.get()

        for e in entities:
            if e.render.renderable:
                if e.has(CollisionComponent):
                    x1, y1 = cartesian_to_screen(e.collide.x1, e.collide.y1, width, height)
                    x2, y2 = cartesian_to_screen(e.collide.x2, e.collide.y2, width, height)

                    pygame.draw.line(screen, BLUE, (x1, y1), (x2, y1))
                    pygame.draw.line(screen, BLUE, (x2, y1), (x2, y2))
                    pygame.draw.line(screen, BLUE, (x1, y2), (x2, y2))
                    pygame.draw.line(screen, BLUE, (x1, y1), (x1, y2))

                if e.has(PositionComponent):
                    x, y = cartesian_to_screen(e.position.x, e.position.y, width, height)
                    pygame.draw.circle(screen, RED, (x, y), 5)