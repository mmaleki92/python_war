from game import Run, Game
from entity import Agent
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