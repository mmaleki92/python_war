# import numpy as np
# import matplotlib.pyplot as plt
import pygame
import pandas as pd

class Game:
    def __init__(self):
        pygame.init()
        self.dis = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('World War!')
        self.clock = pygame.time.Clock()

class Entity:
    def __init__(self, x, y, lx, ly, color, move = True, name = None):
        self.x = x
        self.y = y
        self.lx = lx
        self.ly = ly
        self.color = color
        self.moveable = move
        self.name = name
    def __str__(self):
        return f"x: {self.x}, y: {self.y}, lx : {self.lx}, ly: {self.ly}, color: {self.color}"
    
    def move(self, dx, dy, screen_width, screen_height):
        self.x = (self.x + dx) % screen_width
        self.y = (self.y + dy) % screen_height

class Plotter:
    def __init__(self):
        pass
    def plot(self, entity_list, game, shape):
        if shape == "rect": 
            for obj in entity_list:
                pygame.draw.rect(game.dis, obj.color, [obj.x, obj.y, obj.lx, obj.ly] )
        else:
                pygame.draw.circle(game.dis, obj.color, (obj.x, obj.y), obj.lx )

class Colision:
    def __init__(self):
        pass

    def colide(self, a, b):
        if a.x == b.x and a.y == b.y:
            print("oh no!")

class Run:
    def __init__(self, entity_list):
        self.p = Plotter()
        self.game = Game()
        self.gameover = False
        # self.map = Map()
        self.entities = entity_list #self.map.load_map()
        # self.entities = self.map.map_from_list()
        self.agent = Agent(100, 100, 10, 10, (255, 0, 255))
        self.c = Colision()

    def event_loop(self):
        dx, dy = 0, 0
        while not self.gameover:
            self.game.dis.fill((255, 255, 255))

            self.p.plot(self.entities, self.game, "rect")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameover = True
                if event.type == pygame.KEYDOWN:
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

            self.agent.move(dx=dx, dy=dy, screen_width=self.game.dis.get_width(), screen_height=self.game.dis.get_height()) 
            self.p.plot([self.agent], self.game, "rect")

            for entity in self.entities:
                if entity.moveable:
                    entity.move(dx=0, dy=5, screen_width=self.game.dis.get_width(), screen_height=self.game.dis.get_height())  # Move right by 1 pixel          
                self.c.colide(entity, self.agent)

            pygame.display.update()
            self.game.clock.tick(90)

class Agent(Entity):
    def __init__(self, x, y, lx, ly, color):
        super().__init__(x, y, lx, ly, color)

    def fire(self):
        print(2)

class Map:
    def __init__(self):
        pass

    def load_map(self):
        df = pd.read_csv("map.csv")
        # df = df.reset_index()  # make sure indexes pair with number of rows
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
        pass

    def get_entities_list(self, entity_list, name):
        entity_by_name = [entity for entity in self.entity_list if (entity.name == name)]
        return entity_by_name
  
class Interaction:
    pass

class LimitCheck:
    pass

#TODO
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
    
if __name__ == "__main__":
    r = Run()
    r.event_loop()
