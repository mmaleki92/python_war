import pygame

class Plotter:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.entities = []

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))

    def add_entity(self, entity):
        self.entities.append(entity)

    def remove_entity(self, entity):
        self.entities.remove(entity)

    def update(self):
        # Clear the screen
        self.screen.fill((0, 0, 0))

        # Draw all entities
        for entity in self.entities:
            sprite = pygame.sprite.Sprite()
            sprite.image = entity.image
            sprite.rect = pygame.Rect(entity.x, entity.y, entity.lx, entity.ly)
            self.screen.blit(sprite.image, sprite.rect)

        # Update the display
        pygame.display.flip()

    def run(self, fps):
        clock = pygame.time.Clock()

        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Update and render entities
            self.update()

            # Limit the frame rate
            clock.tick(fps)
