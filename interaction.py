import pygame
import pandas as pd
from entity import Entity, Agent

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
        self.entities = entity_list
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
                    entity.move(dx=0, dy=5, screen_width=self.game.dis.get_width(), screen_height=self.game.dis.get_height())
                self.c.colide(entity, self.agent)

            pygame.display.update()
            self.game.clock.tick(90)

class Builder:
    def __init__(self):
        self.wall_color = (255, 0, 0)
        self.gate_color = (0, 0, 0)

    def wall(self, x, y, lx, ly, move, name):
        return Entity(x, y, lx, ly, self.wall_color, move, name)
    
