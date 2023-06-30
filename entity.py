import math
import pygame
# class MetalWall(Wall):
#     def __init__(self, x, y, lx, ly, color):
#         super().__init__(x, y, lx, ly, color)
#         self.health = 2

# class Metal(Combineable):
#     def __init__(self, x, y, lx, ly, color):
#         super().__init__(x, y, lx, ly, color)

#     def combine(self, other):
#         if isinstance(other, Wall):
#             return MetalWall(other.x, other.y, other.lx, other.ly, other.color)
        
#         return self
# Create a basic wall and a metal object.
# wall = Wall(x=100, y=100, lx=50, ly=50, color=(255, 0, 0))
# metal = Metal(x=150, y=150, lx=25, ly=25, color=(128, 128, 128))

# # Combine the wall and metal objects.
# new_entity = wall.combine(metal)

# # Add the new entity to the list of entities.
# entities = [wall, metal, new_entity]


class Entity:
    MAX_ENTITIES = 300

    def __init__(self, x, y, lx, ly, color, image_path, move=True, name=None):
        # if Entity.num_entities() >= Entity.MAX_ENTITIES:
        #     raise RuntimeError("Cannot create more entities")
        
        self.x = x
        self.y = y
        self.lx = lx
        self.ly = ly
        self.color = color
        self.moveable = move
        self.name = name
        # self.image = pygame.image.load(image_path).convert_alpha()

        Entity.inc_num_entities()

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


    @classmethod
    def num_entities(cls):
        return getattr(cls, "_num_entities", 0)

    @classmethod
    def inc_num_entities(cls):
        cls._num_entities = cls.num_entities() + 1

    @classmethod
    def reset_num_entities(cls):
        setattr(cls, "_num_entities", 0)
    
    def __str__(self):
        return f"x: {self.x}, y: {self.y}, lx : {self.lx}, ly: {self.ly}, color: {self.color}"

    def move(self, dx, dy, screen_width, screen_height):
        self.x = (self.x + dx) % screen_width
        self.y = (self.y + dy) % screen_height

class Agent(Entity):
    MAX_AGENTS = 100
    
    def __init__(self, x, y, lx, ly, color, ammo=10):
        # if Agent.num_agents() >= Agent.MAX_AGENTS:
        #     raise RuntimeError("Cannot create more agents")

        super().__init__(x, y, lx, ly, color, "pic.jpg")
        Agent.inc_num_agents()
        self.ammo = ammo

    @classmethod
    def num_agents(cls):
        return getattr(cls, "_num_agents", 0)

    @classmethod
    def inc_num_agents(cls):
        cls._num_agents = cls.num_agents() + 1

    @classmethod
    def reset_num_agents(cls):
        setattr(cls, "_num_agents", 0)

    def fire(self, target):
        if self.ammo > 0:
            bullet_speed = 20
            dx = target.x - self.x
            dy = target.y - self.y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > 0:
                dx /= dist
                dy /= dist
            else:
                dx = 0
                dy = -1

            b = Bullet(self.x, self.y, dx*bullet_speed, dy*bullet_speed, self.color)
            self.ammo -= 1
            return b
        else:
            return None

class Bullet(Entity):
    def __init__(self, x, y, dx, dy, color):
        super().__init__(x, y, 3, 3, color)
        self.dx = dx
        self.dy = dy
    
    def update(self, dt, screen_width, screen_height, entities):
        # Move bullet
        self.move(self.dx * dt, self.dy * dt, screen_width, screen_height)

        # Check for collisions with entities
        for entity in entities:
            if isinstance(entity, Agent) and entity != self.source_agent:
                if self.collides_with(entity):
                    entity.hit()

        # Check if bullet is offscreen
        if self.is_offscreen(screen_width, screen_height):
            self.dead = True
class Combineable(Entity):
    def combine(self, other):
        raise NotImplementedError("combine() method not implemented.")
    
class Wall(Combineable):
    def __init__(self, x, y, lx, ly, color):
        super().__init__(x, y, lx, ly, color)

    def combine(self, other):
        if isinstance(other, Metal):
            return MetalWall(self.x, self.y, self.lx, self.ly, self.color)
        
        return self

class MetalWall(Wall):
    def __init__(self, x, y, lx, ly, color):
        super().__init__(x, y, lx, ly, color)
        self.health = 2

class Metal(Combineable):
    def __init__(self, x, y, lx, ly, color):
        super().__init__(x, y, lx, ly, color)

    def combine(self, other):
        if isinstance(other, Wall):
            return MetalWall(other.x, other.y, other.lx, other.ly, other.color)
        
        return self
class Wall(Combineable):
    def __init__(self, x, y, lx, ly, color):
        super().__init__(x, y, lx, ly, color)

    def combine(self, other):
        if isinstance(other, Metal):
            return MetalWall(self.x, self.y, self.lx, self.ly, self.color)
        
        return self