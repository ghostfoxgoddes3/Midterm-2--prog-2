class TreeCell(mesa.Agent):
    def __init__(self, pos, model, prob_de_sobrevivencia=0.5):
        """
        Create a new tree with a given probability of survival.
        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
            prob_de_sobrevivencia: Probability of the tree surviving the fire.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Fine"
        self.prob_de_sobrevivencia = prob_de_sobrevivencia  # New attribute
    def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby with a chance of survival.
        """
        if self.condition == "On Fire":
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if neighbor.condition == "Fine":
                    # Check survival probability
                    if self.random.random() > neighbor.prob_de_sobrevivencia:
                        neighbor.condition = "On Fire"
            self.condition = "Burned Out"
import mesa
