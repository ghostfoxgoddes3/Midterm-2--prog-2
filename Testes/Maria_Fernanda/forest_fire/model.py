import mesa

class Cell(mesa.Agent):
    """
    A cell in the forest (can be a tree or a city).

    Attributes:
        x, y: Grid coordinates
        condition: Can be "Fine", "On Fire", "Burned Out", "City", or "Evacuated"
        unique_id: (x,y) tuple.
    """

    def __init__(self, pos, model, city_probability):
        """
        Create a new cell (either a tree or a city).

        Args:
            pos: The cell's coordinates on the grid.
            model: standard model reference for agent.
            city_probability: Probability of this cell being a city.
        """
        super().__init__(pos, model)
        self.pos = pos

        # Decidir se a célula é uma cidade com a probabilidade fornecida
        if self.random.random() < city_probability:
            self.condition = "City"  # A célula é uma cidade
        else:
            self.condition = "Fine"  # A célula é uma árvore
        self.alert = False  # Flag para indicar o alerta de evacuação

    def step(self):
        """
        If the cell is on fire, spread it to fine or city cells nearby.
        If a city is near fire, set alert.
        """
        if self.condition == "On Fire":
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if neighbor.condition == "Fine" or neighbor.condition == "City":
                    neighbor.condition = "On Fire"
            self.condition = "Burned Out"
        
        # Alerta de evacuação para as cidades dentro do raio de 3 células
        if self.condition == "City":
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if neighbor.condition == "On Fire":
                    self.alert = True
                    self.condition = "Evacuated"
                    break


class ForestFire(mesa.Model):
    """
    Simple Forest Fire model with trees and cities, and evacuation alerts.
    """

    def __init__(self, width=100, height=100, density=0.65, city_probability=0.001):
        """
        Create a new forest fire model.

        Args:
            width, height: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
            city_probability: Probability of a cell being a city.
        """
        super().__init__()
        # Set up model objects
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.SingleGrid(width, height, torus=False)

        self.datacollector = mesa.DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
                "City": lambda m: self.count_type(m, "City"),
                "Evacuated": lambda m: self.count_type(m, "Evacuated")
            }
        )

        # Place a tree or a city in each cell with a probability for tree and city
        for contents, (x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                # Create a cell (tree or city)
                new_cell = Cell((x, y), self, city_probability)
                self.grid.place_agent(new_cell, (x, y))
                self.schedule.add(new_cell)

                # Set all cells in the first column on fire, excluding cities
                if x == 0 and new_cell.condition != "City":
                    new_cell.condition = "On Fire"  # Acende as árvores da primeira coluna (excluindo cidades)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Halt if no more fire
        if self.count_type(self, "On Fire") == 0:
            self.running = False

    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count cells in a given condition in a given model.
        """
        count = 0
        for cell in model.schedule.agents:
            if cell.condition == tree_condition:
                count += 1
        return count


