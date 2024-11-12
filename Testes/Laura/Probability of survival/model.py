 def __init__(self, width=100, height=100, density=0.65, prob_de_sobrevivencia=0.5):
        """
        Create a new forest fire model.
        Args:
            width, height: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
            prob_de_sobrevivencia: The probability that a tree survives fire.
        """
        super().__init__()
        # Set up model objects
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.SingleGrid(width, height, torus=False)
        self.prob_de_sobrevivencia = prob_de_sobrevivencia  # Adiciona a probabilidade de sobrevivência
