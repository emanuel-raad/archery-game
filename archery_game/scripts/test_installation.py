def main():
    try:
        import os
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
        print('Pygame installation successful!')
    except:
        print('Pygame installation failed!')

    try:
        from archery_game.engine.components import (CollisionComponent, CollisionType,
                                                    CustomMotionComponent,
                                                    NameComponent, PositionComponent,
                                                    RenderComponent, RotateComponent,
                                                    ShooterComponent,
                                                    VelocityComponent)
        from archery_game.engine.ecs import Entity
        from archery_game.engine.render import WHITE, RenderSystem, gradientRect
        from archery_game.engine.systems import (CollisionSystem, CustomMotionSystem,
                                                 PairedSystem, PhysicsSystem,
                                                 RotateSystem, ScoreSystem,
                                                 ShooterSystem)
        print('Engine installation successful!')
    except:
        print('Engine installation failed!')

if __name__ == '__main__':
    main()