import pygame, pytmx
import itertools

#Background color
BACKGROUND = (20, 20, 20)

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480

#Tiled map layer of tiles that you collide with
MAP_COLLISION_LAYER = 1

class GameMoves(object):
    def __init__(self):
        self.moves = []
    def addMove(self, move):
        self.moves.append(move)
    def getMoves(self):
        for move in self.moves:
            yield move

class Game(object):
    def __init__(self):
        #Set up a level to load
        self.currentLevelNumber = 0
        self.levels = []
        self.levels.append(Level(fileName = "resources/level1.tmx"))
        self.currentLevel = self.levels[self.currentLevelNumber]
        #Create a player object and set the level it is in
        self.player = Player(x = 200, y = 100)
        self.player.currentLevel = self.currentLevel
        self.moves_dict = {"goLeft": self.player.goLeft, "goRight": self.player.goRight, "jump": self.player.jump}

        #Draw aesthetic overlay
        self.overlay = pygame.image.load("resources/overlay.png")
        self.game_moves = GameMoves()
        f = open("logic_upload.txt", "r")
        movement_logic = f.read()
        exec(movement_logic, globals(), locals())
        self.move_gen = self.game_moves.getMoves()
        f.close()
        # create a counter to keep track of the number of moves
        self.move_counter = itertools.count()
    def processEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        # print(self.player.changeX)
        try:
            next_move = next(self.move_gen)
            self.moves_dict[next_move]()
            # print(next_move)
        except StopIteration:
            next_move = None
        
        # if next_move == "goLeft" and self.player.changeX < 0:
        # elif  next_move == "goRight" and self.player.changeX < 20:
        #     self.player.stop()
        # increment the move counter
        if len(self.game_moves.moves) == next(self.move_counter):
            self.player.stop()
        return False
    # def setAgentMovement(self, movement_logic):
        # Execute the provided movement logic

    def runLogic(self):
        #Update player movement and collision logic
        self.player.update()
    
    #Draw level, player, overlay
    def draw(self, screen):
        screen.fill(BACKGROUND)
        self.currentLevel.draw(screen)
        self.player.draw(screen)
        screen.blit(self.overlay, [0, 0])
        pygame.display.flip()
        # print every 100 frames
        if pygame.time.get_ticks() % 60 == 0:
                
            for tile in self.player.annotatedTiles:
                # print(dir(tile))
                print("Annotated Tile Position:", tile.rect.x, tile.rect.y)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.annotatedTiles = []
        #Load the spritesheet of frames for this player
        self.sprites = SpriteSheet("resources/player.png")
    
        self.stillRight = self.sprites.image_at((0, 0, 30, 42))
        self.stillLeft = self.sprites.image_at((0, 42, 30, 42))
        
        #List of frames for each animation
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
        
        #Set player position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        #Set speed and direction
        self.changeX = 0
        self.changeY = 0
        self.direction = "right"
        
        #Boolean to check if player is running, current running frame, and time since last frame change
        self.running = False
        self.runningFrame = 0
        self.runningTime = pygame.time.get_ticks()
        
        #Players current level, set after object initialized in game constructor
        self.currentLevel = None
        
    def update(self):
        #Update player position by change
        self.rect.x += self.changeX

        #Get tiles in collision layer that player is now touching
        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        #Move player to correct side of that block
        for tile in tileHitList:
            if self.changeX > 0:
                self.rect.right = tile.rect.left
            else:
                self.rect.left = tile.rect.right
            self.annotatedTiles.append(tile)

        #Move screen if player reaches screen bounds
        if self.rect.right >= SCREEN_WIDTH - 200:
            difference = self.rect.right - (SCREEN_WIDTH - 200)
            self.rect.right = SCREEN_WIDTH - 200
            self.currentLevel.shiftLevel(-difference)
        
        #Move screen is player reaches screen bounds
        if self.rect.left <= 200:
            difference = 200 - self.rect.left
            self.rect.left = 200
            self.currentLevel.shiftLevel(difference)
        
        #Update player position by change
        self.rect.y += self.changeY

        #Get tiles in collision layer that player is now touching
        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
       
        #If there are tiles in that list
        if len(tileHitList) > 0:
            #Move player to correct side of that tile, update player frame
            for tile in tileHitList:
                if self.changeY > 0:
                    self.rect.bottom = tile.rect.top
                    self.changeY = 1
                    
                    if self.direction == "right":
                        self.image = self.stillRight
                    else:
                        self.image = self.stillLeft
                else:
                    self.rect.top = tile.rect.bottom
                    self.changeY = 0
        #If there are not tiles in that list
        else:
            #Update player change for jumping/falling and player frame
            self.changeY += 0.2
            if self.changeY > 0:
                if self.direction == "right":
                    self.image = self.jumpingRight[1]
                else:
                    self.image = self.jumpingLeft[1]
        #If player is on ground and running, update running animation
        if self.running and self.changeY == 1:
            if self.direction == "right":
                self.image = self.runningRight[self.runningFrame]
            else:
                self.image = self.runningLeft[self.runningFrame]
        
        #When correct amount of time has passed, go to next frame
        if pygame.time.get_ticks() - self.runningTime > 50:
            self.runningTime = pygame.time.get_ticks()
            if self.runningFrame == 4:
                self.runningFrame = 0
            else:
                self.runningFrame += 1

    #Make player jump
    def jump(self):
        #Check if player is on ground
        self.rect.y += 2
        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        self.rect.y -= 2
        
        if len(tileHitList) > 0:
            if self.direction == "right":
                self.image = self.jumpingRight[0]
            else:
                self.image = self.jumpingLeft[0]
                
            self.changeY = -6
    
    #Move right
    def goRight(self):
        self.direction = "right"
        self.running = True
        self.changeX = 3
    
    #Move left
    def goLeft(self):
        self.direction = "left"
        self.running = True
        self.changeX = -3
    
    #Stop moving
    def stop(self):
        self.running = False
        self.changeX = 0
    
    #Draw player
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
class Level(object):
    def __init__(self, fileName):
        #Create map object from PyTMX
        self.mapObject = pytmx.load_pygame(fileName)
        
        #Create list of layers for map
        self.layers = []
        
        #Amount of level shift left/right
        self.levelShift = 0
        
        #Create layers for each layer in tile map
        for layer in range(len(self.mapObject.layers)):
            self.layers.append(Layer(index = layer, mapObject = self.mapObject))
    
    #Move layer left/right
    def shiftLevel(self, shiftX):
        self.levelShift += shiftX
        
        for layer in self.layers:
            for tile in layer.tiles:
                tile.rect.x += shiftX
    
    #Update layer
    def draw(self, screen):
        for layer in self.layers:
            layer.draw(screen)
            
class Layer(object):
    def __init__(self, index, mapObject):
        #Layer index from tiled map
        self.index = index
        
        #Create gruop of tiles for this layer
        self.tiles = pygame.sprite.Group()
        
        #Reference map object
        self.mapObject = mapObject
        
        #Create tiles in the right position for each layer
        for x in range(self.mapObject.width):
            for y in range(self.mapObject.height):
                img = self.mapObject.get_tile_image(x, y, self.index)
                if img:
                    self.tiles.add(Tile(image = img, x = (x * self.mapObject.tilewidth), y = (y * self.mapObject.tileheight)))

    #Draw layer
    def draw(self, screen):
        self.tiles.draw(screen)

#Tile class with an image, x and y
class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#Sprit sheet class to load sprites from player spritesheet
class SpriteSheet(object):
    def __init__(self, fileName):
        self.sheet = pygame.image.load(fileName)

    def image_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        return image

def main():
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("Pygame Tiled Demo")
    clock = pygame.time.Clock()
    done = False
    game = Game()
    
    while not done:
        game.runLogic()
        done = game.processEvents()
        game.draw(screen)
        clock.tick(60)

    pygame.quit()

main()