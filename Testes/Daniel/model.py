import mesa
from agent import TreeCell, Police, Bomber, Logger

class ForestFire(mesa.Model):
    """
    Simple Forest Fire model.
    """

    def __init__(self, width=100, height=100, density=0.65, prob_de_sobrevivencia=0.5, num_policiais=5, num_bombers=3, num_loggers=3):
        """
        Create a new forest fire model.

        Args:
            width, height: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
            prob_de_sobrevivencia: The probability that a tree survives fire.
        """
        super().__init__()
        # Set up model objects
        self.schedule = mesa.time.RandomActivationByType(self)
        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.prob_de_sobrevivencia = prob_de_sobrevivencia  # Add survival probability
        self.datacollector = mesa.DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
                "Fire Off": lambda m: self.count_type(m, "Fire Off"),
                "Toasted": lambda m: self.count_type(m, "Toasted")
            }
        )

        # Place a tree in each cell with Prob = density
        for contents, (x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                # Create a tree
                new_tree = TreeCell((x, y), self)
                # Set all trees in the first column on fire.
                if x == 0:
                    new_tree.condition = "On Fire"
                self.grid.place_agent(new_tree, (x, y))
                self.schedule.add(new_tree)

        # Place police officers in the grid
        for _ in range(num_policiais):
            x = self.random.randint(0, self.grid.width - 1)
            y = self.random.randint(0, self.grid.height - 1)
            new_police = Police((x, y), self, range_view=3)
            self.grid.place_agent(new_police, (x, y))
            self.schedule.add(new_police)

        # Place Bombers in the grid
        for _ in range(num_bombers):
            x = self.random.randint(0, self.grid.width - 1)
            y = self.random.randint(0, self.grid.height - 1)
            new_Bomber = Bomber(
                (x, y), 
                self, 
                bomb_radius=2,  # Bombing radius
                speed=1  
            )
            self.grid.place_agent(new_Bomber, (x, y))
            self.schedule.add(new_Bomber)

        # Place loggers in the grid
        for _ in range(num_loggers):
            x = self.random.randint(0, self.grid.width - 1)
            y = self.random.randint(0, self.grid.height - 1)
            new_logger = Logger((x, y), self)
            self.grid.place_agent(new_logger, (x, y))
            self.schedule.add(new_logger)

    def step(self):  
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # Collect data for analysis
        self.datacollector.collect(self)

        # If no trees are on fire, stop the simulation
        if self.count_type(self, "On Fire") == 0:
            self.running = False

    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, TreeCell) and agent.condition == tree_condition:
                count += 1
        return count
