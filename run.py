class Run:
    def __init__(self, agents, entities):
        self.p = Plotter()
        self.game = Game()
        self.gameover = False
        self.agents = agents
        self.entities = entities
        self.c = Colision()

    def event_loop(self):
        while not self.gameover:
            self.game.dis.fill((255, 255, 255))

            # Draw entities and agents
            self.p.plot(self.entities + self.agents, self.game.dis, "rect")

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameover = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.gameover = True
                    elif event.key == pygame.K_SPACE:
                        for agent in self.agents:
                            target = self.find_nearest_enemy(agent)
                            if target is not None:
                                bullet = agent.fire(target)
                                if bullet is not None:
                                    self.entities.append(bullet)

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
                
                agent.move(dx=dx, dy=dy, screen_width=self.game.dis.get_width(), screen_height=self.game.dis.get_height())

            # Move entities and check for collisions with agents
            for entity in self.entities:
                if entity.moveable:
                    entity.move(dx=0, dy=5, screen_width=self.game.dis.get_width(), screen_height=self.game.dis.get_height())
                for agent in self.agents:
                    self.c.colide(entity, agent)

            # Update display
            pygame.display.update()
            self.game.clock.tick(90)

    def find_nearest_enemy(self, agent):
        min_dist = float('inf')
        nearest_enemy = None
        for other_agent in self.agents:
            if other_agent != agent:
                dist = math.sqrt((agent.x - other_agent.x)**2 + (agent.y - other_agent.y)**2)
                if dist < min_dist:
                    min_dist = dist
                    nearest_enemy = other_agent
        return nearest_enemy
    