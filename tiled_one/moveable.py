import pygame, pytmx

# Background color
BACKGROUND = (20, 20, 20)

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480

# Tiled map layer of tiles that you collide with
MAP_COLLISION_LAYER = 1

class Game(object):
    def __init__(self):
        # Set up a level to load
        self.currentLevelNumber = 0
        self.levels = []
        self.levels.append(Level(fileName="resources/level1.tmx"))
        self.currentLevel = self.levels[self.currentLevelNumber]

        # Create a player object and set the level it is in
        self.player = Player(x=200, y=100)
        self.player.currentLevel = self.currentLevel

        # Draw aesthetic overlay
        self.overlay = pygame.image.load("resources/overlay.png")

    def processEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            
        return False

    def runLogic(self):
        # Update player movement and collision logic
        self.player.update()

    # Draw level, player, overlay
    def draw(self, screen):
        screen.fill(BACKGROUND)
        self.currentLevel.draw(screen)
        self.player.draw(screen)
        screen.blit(self.overlay, [0, 0])
        pygame.display.flip()

    def setAgentMovement(self, movement_logic):
        game = Game()

        # Execute the provided movement logic
        exec(movement_logic, globals(), locals())

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Load the spritesheet of frames for this player
        self.sprites = SpriteSheet("resources/player.png")

        self.stillRight = self.sprites.image_at((0, 0, 30, 42))
        self.stillLeft = self.sprites.image_at((0, 42, 30, 42))

        # List of frames for each animation
        self.runningRight = (self.sprites.image_at((0, 84, 30, 42)),
                              self.sprites.image_at((30, 84, 30, 42)),
                              self.sprites.image_at((60, 84, 30, 42)),
                              self.sprites.image_at((90, 84, 30, 42)),
                              self.sprites.image_at((120, 84, 30, 42)))

        self.runningLeft = (self.sprites.image_at((0, 126, 30, 42)),
                             self.sprites.image_at((30, 126, 30, 42)),
                             self.sprites.image_at((60, 126, 30, 42)),
                             self.sprites.image_at((90, 126, 30, 42)),
                             self.sprites.image_at((120, 126, 30, 42)))

        self.jumpingRight = (self.sprites.image_at((30, 0, 30, 42)),
                              self.sprites.image_at((60, 0, 30, 42)),
                              self.sprites.image_at((90, 0, 30, 42)))

        self.jumpingLeft = (self.sprites.image_at((30, 42, 30, 42)),
                             self.sprites.image_at((60, 42, 30, 42)),
                             self.sprites.image_at((90, 42, 30, 42)))

        self.image = self.stillRight

        # Set player position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Set initial player velocity
        self.changeX = 0
        self.changeY = 0

        self.walkingFrames = 4
        self.jumpingFrames = 2

        # Set player direction
        self.direction = "R"

        # Player's current level
        self.currentLevel = None

    def update(self):
        self.calcGrav()

        # Move left/right
        self.rect.x += self.changeX

        # Check for collision with walls
        wallCollisionSprites = pygame.sprite.spritecollide(self, self.currentLevel.walls, False)
        for wall in wallCollisionSprites:
            if self.changeX > 0:
                self.rect.right = wall.rect.left
            elif self.changeX < 0:
                self.rect.left = wall.rect.right

        # Move up/down
        self.rect.y += self.changeY

        # Check for collision with walls
        wallCollisionSprites = pygame.sprite.spritecollide(self, self.currentLevel.walls, False)
        for wall in wallCollisionSprites:
            if self.changeY > 0:
                self.rect.bottom = wall.rect.top
            elif self.changeY < 0:
                self.rect.top = wall.rect.bottom

            self.changeY = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    # Calculate effect of gravity
    def calcGrav(self):
        if self.changeY == 0:
            self.changeY = 1
        else:
            self.changeY += 0.35

        # Check if on the ground
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.changeY >= 0:
            self.changeY = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

class Level(object):
    def __init__(self, fileName):
        self.fileName = fileName

        # Create a list to hold all the sprite objects
        self.allSprites = pygame.sprite.Group()

        # Create a list of walls
        self.walls = pygame.sprite.Group()

        # Load the level from the file
        self.loadLevelFromFile()

    def loadLevelFromFile(self):
        tm = pytmx.load_pygame(self.fileName)

        # Create the walls based on the Tiled map data
        for object in tm.objects:
            if object.type == "wall":
                wall = pygame.sprite.Sprite()
                wall.rect = pygame.Rect(object.x, object.y, object.width, object.height)
                self.walls.add(wall)

        self.allSprites.add(self.walls)

    def draw(self, screen):
        self.allSprites.draw(screen)

class SpriteSheet(object):
    def __init__(self, fileName):
        self.sheet = pygame.image.load(fileName).convert()

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)

        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)

        return image

def main():
    pygame.init()
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Agent Movement Example")
    done = False
    clock = pygame.time.Clock()

    game = Game()
    movement_logic = """
    
# Custom movement logic
if True:
    game.player.changeX = -5  # Move left
elif condition:
    game.player.changeX = 5   # Move right
else:
    game.player.changeX = 0   # Stop moving horizontally
    """

    game.setAgentMovement(movement_logic)
    while not done:
        done = game.processEvents()
        game.runLogic()
        game.draw(screen)
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()