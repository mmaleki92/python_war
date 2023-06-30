import pygame
from interaction import Plotter, Colision
from entity import Agent
from map import Map

class Game:
    def __init__(self, num_agents):
        self.num_agents = num_agents
        pygame.init()
        self.dis = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('World War!')
        self.clock = pygame.time.Clock()
        self.agent_colors = [(255, 0, 255), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 0)]
        self.entity_colors = [(0, 255, 255), (255, 255, 255), (128, 128, 128), (128, 0, 128), (0, 128, 0)]
        self.agents = []
        self.entities = []

        for i in range(num_agents):
            self.agents.append(Agent(100 * (i+1), 100, 10, 10, (255,0,255)))# self.agent_colors[i]))

        # Load map from file
        self.map = Map().load_map()

    def run(self):
        p = Plotter()
        c = Colision()
        while True:
            self.dis.fill((255, 255, 255))

            # Draw entities and agents
            p.plot(self.entities + self.agents, self.dis, "rect")

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

            # Move agents
            for agent in self.agents:
                dx, dy = 0, 0
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    dy = -5
                if keys[pygame.K_s]:
                    dy = 5
                if keys[pygame.K_a]:
                    dx = -5
                if keys[pygame.K_d]:
                    dx = 5
                
                agent.move(dx=dx, dy=dy, screen_width=self.dis.get_width(), screen_height=self.dis.get_height())

            # Move entities and check for collisions with agents
            for entity in self.entities:
                if entity.moveable:
                    entity.move(dx=0, dy=5, screen_width=self.dis.get_width(), screen_height=self.dis.get_height())
                for agent in self.agents:
                    c.colide(entity, agent)

            # Update display
            pygame.display.update()
            self.clock.tick(90)
            
class Run:
    def __init__(self, agents, entities):
        self.p = Plotter()
        self.game = Game(100)
        self.gameover = False
        self.agents = agents
        self.entities = entities
        self.c = Colision()
    # def event_loop(self):
    #     while not self.gameover:
    #         self.game.dis.fill((255, 255, 255))

    #         # Draw entities and agents
    #         self.p.plot(self.entities + self.agents, self.game.dis, "rect")

    #         # Handle events
    #         for event in pygame
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

            self.agents.move(dx=dx, dy=dy, screen_width=self.game.dis.get_width(), screen_height=self.game.dis.get_height()) 
            self.p.plot([self.agents], self.game, "rect")

            for entity in self.entities:
                if entity.moveable:
                    entity.move(dx=0, dy=5, screen_width=self.game.dis.get_width(), screen_height=self.game.dis.get_height())  # Move right by 1 pixel          
                self.c.colide(entity, self.agents)

            pygame.display.update()
            self.game.clock.tick(90)