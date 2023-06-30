class UserAgent(Agent):
    def __init__(self, x, y, lx, ly, color, ammo, behavior_fn):
        super().__init__(x, y, lx, ly, color, ammo)
        self.behavior_fn = behavior_fn

    def get_movement(self, entities):
        return self.behavior_fn(self, entities)

# Example behavior function that moves the agent towards the nearest enemy.
def chase_enemy(agent, entities):
    target = None
    min_dist = float('inf')
    for entity in entities:
        if isinstance(entity, Agent) and entity != agent:
            dist = math.sqrt((entity.x - agent.x)**2 + (entity.y - agent.y)**2)
            if dist < min_dist:
                target = entity
                min_dist = dist
    
    if target is not None:
        dx = target.x - agent.x
        dy = target.y - agent.y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > 0:
            dx /= dist
            dy /= dist
        else:
            dx = 0
            dy = -1
    else:
        dx = 0
        dy = 0
    
    return dx*5, dy*5
agent_behavior = chase_enemy  # Replace with your own behavior function.

user_agent = UserAgent(x=100, y=100, lx=10, ly=10, color=(255, 0, 255), ammo=10, behavior_fn=agent_behavior)
agents = [user_agent]  # Add any other agents as needed.

game = Game(num_agents=len(agents))
run = Run(agents=agents, entities=game.entities)
run.event_loop()


class UserAgent(Agent):
    def __init__(self, x, y, lx, ly, color, ammo, behaviors):
        super().__init__(x, y, lx, ly, color, ammo)
        self.behaviors = behaviors

    def get_movement(self, entities):
        dx, dy = 0, 0
        
        for behavior in self.behaviors:
            move = behavior(self, entities)
            dx += move[0]
            dy += move[1]
        
        # Normalize movement vector
        dist = math.sqrt(dx**2 + dy**2)
        if dist > 0:
            dx /= dist
            dy /= dist
        
        return dx*5, dy*5

# # Example behavior function that avoids walls.
# def avoid_walls(agent, entities):
#     wall_distance = 30  # Minimum distance from walls to avoid collision
#     padding = 10  # Padding around agent bounding box
    
#     # Calculate bounding box around agent
#     left = agent.x - agent.lx/2 - padding
#     right = agent.x + agent.lx/2 + padding
#     top = agent.y - agent.ly/2 - padding
#     bottom = agent.y + agent.ly/2 + padding
    
#     # Check for collisions with walls
#     dx, dy = 0, 0
#     for entity in entities:
#         if isinstance(entity, Wall):
#             if left < entity.x + entity.lx and right > entity.x and top < entity.y + entity.ly and bottom > entity.y:
#                 if agent.x <= entity.x:
#                     dx -= wall_distance
#                 elif agent.x >= entity.x + entity.lx:
#                     dx += wall_distance
                
#                 if agent.y <= entity.y:
#                     dy -= wall_distance
#                 elif agent.y >= entity.y + entity.ly:
#                     dy += wall_distance
    
#     return dx, dy

# agent_behaviors = [chase_enemy, avoid_walls]  # Replace with your own list of behavior functions.

# user_agent = UserAgent(x=100, y=100, lx=10, ly=10, color=(255, 0, 255), ammo=10, behaviors=agent_behaviors)
# agents = [user_agent]  # Add any other agents as needed.

# game = Game(num_agents=len(agents))
# run = Run(agents=agents, entities=game.entities)
# run.event_loop()