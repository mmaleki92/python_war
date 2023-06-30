import pygame
import pandas as pd
import math

class Collision:
    def __init__(self):
        pass

    def collide(self, a, b):
        if isinstance(a, Bullet) and isinstance(b, Wall):
            # If a bullet hits a wall, destroy the bullet
            a.active = False
        elif isinstance(a, Bullet) and isinstance(b, Enemy):
            # If a bullet hits an enemy, destroy the bullet and damage the enemy
            a.active = False
            b.health -= 10

class Game:
    def __init__(self):
        pygame.init()
        self.dis = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('World War!')
        self.clock = pygame.time.Clock()

class Entity:
    def __init__(self, x, y, lx, ly, color, move, name):
        self.x = x
        self.y = y
        self.lx = lx
        self.ly = ly
        self.color = color
        self.dx = 0

        self.dy = 0
        self.moveable = move
        self.name = name
    def move(self, dx, dy, screen_width, screen_height):
        self.x = (self.x + dx) % screen_width
        self.y = (self.y + dy) % screen_height

class Plotter:
    def __init__(self):
        pass
    def plot(self, entity_list, game, shape):
        if shape == "rect": 
            for obj in entity_list:
                game.dis.blit(bullet_image, (obj.x, obj.y))
                # pygame.draw.rect(game.dis, obj.color, [obj.x, obj.y, obj.lx, obj.ly] )
        else:
                game.dis.blit(bullet_image, (obj.x, obj.y))
                # pygame.draw.circle(game.dis, obj.color, (obj.x, obj.y), obj.lx )

# class Colision:
#     def __init__(self):
#         pass

#     def colide(self, a, b):
#         if a.x == b.x and a.y == b.y:
#             print("oh no!")

class Enemy(Entity):
    def __init__(self, x, y, lx, ly, color=(0, 255, 0), health=100):
        super().__init__(x, y, lx, ly, color, True, "enemy")
        self.health = health

    def move(self, screen_width, screen_height):
        # Enemy movement logic goes here
        pass

class Wall(Entity):
    def __init__(self, x, y, lx, ly, color=(200, 200, 200)):
        super().__init__(x, y, lx, ly, color, False, "wall")
        
class Run:
    def __init__(self, entity_list):
        self.p = Plotter()
        self.game = Game()
        self.gameover = False
        # self.map = Map()
        self.entities = entity_list #self.map.load_map()
        # self.entities = self.map.map_from_list()
        self.agent = Agent(100, 100, 20, 20, (255, 0, 255), True, "agent", behavior_function=chase_closest_enemy)

        # self.agent = Agent(100, 100, 10, 10, (255, 0, 255), True, "agent")
        self.c = Collision()

    def event_loop(self):
        dx, dy = 0, 0
        while not self.gameover:
            self.game.dis.fill((255, 255, 255))

            self.p.plot(self.entities, self.game, "rect")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameover = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.agent.fire(dx, dy)

                    if event.key == pygame.K_w:
                        dx = 0
                        dy = -5
                    if event.key == pygame.K_s:
                        dx = 0
                        dy = 5
                    if event.key == pygame.K_a:
                        dx = -5
                        dy = 0
                    if event.key == pygame.K_d:
                        dx = 5
                        dy = 0
                        
            for bullet in self.agent.bullets:
                if bullet.active:
                    bullet.move(screen_width=self.game.dis.get_width(), screen_height=self.game.dis.get_height())
                    self.c.collide(bullet, self.entities)
            self.agent.bullets = [bullet for bullet in self.agent.bullets if bullet.active]
            self.agent.move_bullets(screen_width=self.game.dis.get_width(), screen_height=self.game.dis.get_height())
            self.agent.clear_inactive_bullets(screen_height=self.game.dis.get_height(), screen_width=self.game.dis.get_width())
            self.agent.draw_bullets(game=self.game)
             
            self.agent.behave(self.entities)

            self.agent.move(dx=dx, dy=dy, screen_width=self.game.dis.get_width(), screen_height=self.game.dis.get_height()) 
            self.p.plot([self.agent], self.game, "rect")

            for entity in self.entities:
                if entity.moveable:
                    entity.move(dx=0, dy=5, screen_width=self.game.dis.get_width(), screen_height=self.game.dis.get_height())  # Move right by 1 pixel          
                self.c.collide(entity, self.agent)

            pygame.display.update()
            self.game.clock.tick(90)

bullet_image = pygame.image.load("bullet.png")
# Set the desired width and height for the resized image
new_width = 20
new_height = 20

# Resize the image using pygame.transform.scale()
bullet_image = pygame.transform.scale(bullet_image, (new_width, new_height))
class Agent(Entity):
    def __init__(self, x, y, lx, ly, color, move, name, behavior_function = None):
        super().__init__(x, y, lx, ly, color, move, name)
        self.bullets = []
        self.game = Game()
        self.behavior_function = behavior_function

    def behave(self, entities):
        if self.behavior_function:
            self.behavior_function(self, entities)
    def fire(self, dx=0, dy=-10):
        bullet_pos = (self.x + self.lx // 2, self.y + self.ly // 2)
        bullet = Bullet(*bullet_pos, dx=dx*2, dy=dy*2)
        self.bullets.append(bullet) 
        # bullet = Entity(*bullet_pos, 5, 5, (255, 0, 0), True, "bullet")
        bullet.dx = dx * 2
        bullet.dy = dy * 2
        self.bullets.append(bullet)

    def draw_bullets(self, game):
        for bullet in self.bullets:
            game.dis.blit(bullet_image, (bullet.x, bullet.y))
            # pygame.draw.rect(game.dis, bullet.color, [bullet.x, bullet.y, bullet.lx, bullet.ly])
    
    def move_bullets(self, screen_width, screen_height):
        for bullet in self.bullets:
            bullet.move(screen_width, screen_height)

    def clear_inactive_bullets(self, screen_height, screen_width):
        self.bullets = [bullet for bullet in self.bullets if
                        (bullet.ly+2 <= bullet.y <=  screen_height - bullet.ly-1) and
                        (bullet.lx+2 <= bullet.x <= screen_width - bullet.lx-1)]

class Map:
    def __init__(self):
        pass

    def load_map(self):
        df = pd.read_csv("map.csv")
        obj_list  = []
        for x, y, lx, ly, r, g, b in zip(df["x"], df["y"],df["lx"],df["ly"],df["r"],df["g"],df["b"]):
            obj_list.append(Entity(x, y, lx, ly, (r, g, b)))
        return obj_list
    
    def map_from_list(self, map_list):
        return map_list

class Builder:
    def __init__(self):
        self.wall_color = (255, 0, 0)
        self.gate_color = (0, 0, 0)

    def wall(self, x, y, lx, ly, move, name):
        return Entity(x, y, lx, ly, self.wall_color, move, name)
    
    def gate(self,x, y, lx, ly, move, name):
        return Entity(x, y, lx, ly, self.gate_color, move, name)

class CoordinationCenter:
    def __init__(self):
        self.players = []
        self.stats = {}

    def add_player(self, player):
        self.players.append(player)
        self.stats[player.name] = {"score": 0, "health": 100}

    def update_score(self, player, score):
        self.stats[player.name]["score"] += score

    def update_health(self, player, health):
        self.stats[player.name]["health"] = health

    def get_player_stats(self, player):
        return self.stats[player.name]

    def get_total_score(self):
        total_score = sum([player_stats["score"] for player_stats in self.stats.values()])
        return total_score

    def get_average_health(self):
        total_health = sum([player_stats["health"] for player_stats in self.stats.values()])
        average_health = total_health / len(self.players)
        return average_health
    
    def get_entities_list(self, entity_list, name):
        entity_by_name = [entity for entity in self.entity_list if (entity.name == name)]
        return entity_by_name
  
class Interaction:
    pass

class LimitCheck:
    pass

class Bullet(Entity):
    def __init__(self, x, y, dx, dy):
        super().__init__(x, y, 5, 5, (255, 0, 0), True, "bullet")
        self.dx = dx
        self.dy = dy
        self.active = True

    def move(self, screen_width, screen_height):
        self.x += self.dx
        self.y += self.dy
        if self.x < 0 or self.x > screen_width or self.y < 0 or self.y > screen_height:
            # If the bullet goes offscreen, mark it as inactive
            self.active = False

class War:
    def __init__(self):
        self.coor_center = CoordinationCenter()
        self.map = Map()

    def add_equip(self, map):
        self.equip = self.map.map_from_list(map)
        self.coor_center = self.equip

    def start(self):
        r = Run(self.equip)
        r.event_loop()


def chase_closest_enemy(agent, entities):
    closest_enemy = None
    closest_distance = float('inf')
    for entity in entities:
        if entity != agent and isinstance(entity, Entity) and not entity.moveable:
            distance = math.sqrt((entity.x - agent.x) ** 2 + (entity.y - agent.y) ** 2)
            if distance < closest_distance:
                closest_enemy = entity
                closest_distance = distance
    
    if closest_enemy:
        dx = closest_enemy.x - agent.x
        dy = closest_enemy.y - agent.y
        norm = math.sqrt(dx**2 + dy**2)
        if norm > 0:
            dx /= norm
            dy /= norm
        agent.move(dx=dx*5, dy=dy*5, screen_width=800, screen_height=600)        

if __name__ == "__main__":
    war = War()
    build = Builder()
    f = []
    for i in range(100, 1000, 100):
        wall = build.wall(i, 400, 10, 10, True, "wall")
        f.append(wall)
    war.add_equip(f)
    war.start()
