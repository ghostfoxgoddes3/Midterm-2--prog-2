import mesa
from agent import TreeCell
from bombeiro import GroundFirefighter

class ForestFire(mesa.Model):
    def __init__(self, width=100, height=100, density=0.65):
        super().__init__()
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.SingleGrid(width, height, torus=False)

        # Adiciona o bombeiro
        firefighter_position = (self.random.randrange(width), self.random.randrange(height))
        firefighter = GroundFirefighter(self.next_id(), self, firefighter_position)
        self.grid.place_agent(firefighter, firefighter_position)
        self.schedule.add(firefighter)

        # Cria as árvores
        for x in range(width):
            for y in range(height):
                if self.random.random() < density and self.grid.is_cell_empty((x, y)):
                    new_tree = TreeCell((x, y), self)
                    if x == 0:  # Coloca fogo na linha inicial
                        new_tree.condition = "On Fire"
                    self.grid.place_agent(new_tree, (x, y))
                    self.schedule.add(new_tree)

        # Coleta de dados
        self.datacollector = mesa.DataCollector(
            {
                "Fine": lambda m: sum(1 for agent in m.schedule.agents if isinstance(agent, TreeCell) and agent.condition == "Fine"),
                "On Fire": lambda m: sum(1 for agent in m.schedule.agents if isinstance(agent, TreeCell) and agent.condition == "On Fire"),
                "Burned Out": lambda m: sum(1 for agent in m.schedule.agents if isinstance(agent, TreeCell) and agent.condition == "Burned Out"),
                "Fire Off": lambda m: sum(1 for agent in m.schedule.agents if isinstance(agent, TreeCell) and agent.condition == "Fire Off")
            }
        )

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

        # Finaliza quando não há mais fogo
        if self.datacollector.get_agent_vars_dataframe()["On Fire"][-1] == 0:
            self.running = False
