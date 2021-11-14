import operator
from math import cos, degrees, sin
from copy import copy

import pygame
from archery_game.engine.components import (CollisionComponent,
                                            PositionComponent, RenderComponent,
                                            RotateComponent)
from archery_game.engine.ecs import System
from archery_game.engine.systems import cartesian_to_screen

WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255, 0, 0)

def gradientRect(target_rect, left_colour, right_colour):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    # https://stackoverflow.com/a/62336993
    colour_rect = pygame.Surface( ( 2, 2 ) )                                   # tiny! 2x2 bitmap
    pygame.draw.line( colour_rect, left_colour,  ( 0,0 ), ( 0,1 ) )            # left colour line
    pygame.draw.line( colour_rect, right_colour, ( 1,0 ), ( 1,1 ) )            # right colour line
    colour_rect = pygame.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) )  # stretch!
    return colour_rect

class RenderSystem(System):
    def __init__(self):
        super().__init__()

        self.subscribe(RenderComponent)

    @staticmethod
    def rotatePivoted(im, angle, pivot):
        # rotate the leg image around the pivot
        image = pygame.transform.rotate(im, angle)
        rect = image.get_rect()
        rect.center = pivot
        return image, rect

    def update(self, screen, width, height):
        entities = self.get()
        entities = sorted(entities, key=operator.attrgetter('render.priority'))

        for e in entities:
            if e.render.renderable:
                # Draw the sprite
                if e.has(PositionComponent) and e.render.path is not None:

                    # Cache the original image instead of reading it from the file every loop
                    if not hasattr(e.render, '_cached_img'):
                        img = pygame.image.load(e.render.path).convert_alpha()
                        e.render._cached_img = copy(img)
                    else:
                        img = e.render._cached_img

                    x, y = cartesian_to_screen(e.position.x, e.position.y, width, height)
                    rect = None

                    if e.render.size is not None:
                        img = pygame.transform.scale(img, e.render.size)

                    cx, cy = 0, 0
                    if e.render.center is not None:
                        cx, cy = e.render.center

                    if e.has(RotateComponent) and e.render.center is not None:
                        angle = e.rotate.ut
                        img, rect = self.rotatePivoted(img, degrees(angle), (x, y))
                        rect.centerx -= e.render.center[0] / 2 * cos(angle)
                        rect.centery += e.render.center[1] * 2 * sin(angle)

                    if rect is not None:
                        screen.blit(img, rect)
                    else:
                        screen.blit(img, (x - cx, y - cy))

                # Draw the position
                if e.has(PositionComponent) and e.render.debug:
                    x, y = cartesian_to_screen(e.position.x, e.position.y, width, height)
                    pygame.draw.circle(screen, RED, (x, y), 5)

                # Draw the bounding box
                if e.has(CollisionComponent) and e.render.debug:
                    x1, y1 = cartesian_to_screen(e.collide.x1, e.collide.y1, width, height)
                    x2, y2 = cartesian_to_screen(e.collide.x2, e.collide.y2, width, height)

                    pygame.draw.circle(screen, BLUE, (x1, y1), 5)
                    pygame.draw.circle(screen, BLUE, (x1, y2), 5)
                    pygame.draw.circle(screen, BLUE, (x2, y1), 5)
                    pygame.draw.circle(screen, BLUE, (x2, y2), 5)

                    pygame.draw.line(screen, BLUE, (x1, y1), (x2, y1))
                    pygame.draw.line(screen, BLUE, (x2, y1), (x2, y2))
                    pygame.draw.line(screen, BLUE, (x1, y2), (x2, y2))
                    pygame.draw.line(screen, BLUE, (x1, y1), (x1, y2))