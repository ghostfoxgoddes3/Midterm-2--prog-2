# Updates
- Aqui serão incluídos apenas os updates essenciais feitos, no código, por mim. Mas, em resumo:

Criei e implementei a probabilidade de sobrevivência nas três partes do código.







## Update 1 - prob_de_sobrevivencia agent

- Segue abaixo a alteração feita no código


import mesa

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

   

## Update 2 - prob_de_sobrevivencia - model

- Segue abaixo a alteração feita no código
  

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


  
## Update 3 - prob_de_sobrevivencia - server

- Segue abaixo a alteração feita no código


model_params = {
    "height": 100,
    "width": 100,
    "density": mesa.visualization.Slider("Tree density", 0.65, 0.01, 1.0, 0.01),
    "prob_de_sobrevivencia": mesa.visualization.Slider("Probability of survival", 0.5, 0.0, 1.0, 0.01)
}

server = mesa.visualization.ModularServer(
    ForestFire, [canvas_element, tree_chart, pie_chart], "Forest Fire", model_params
)

server.port = 8521  # Porta do servidor
server.launch()



## Update 4 - prob_de_sobrevivencia - agent

- Segue abaixo a alteração feita no código

        self.model = model
        self.condition = "Fine"  # Possíveis condições: "Fine", "On Fire", "Burned Out"
        self.prob_de_sobrevivencia = prob_de_sobrevivencia


   print(f"Tree at {self.pos} is on fire, spreading fire to neighbors...")
            for neighbor in self.model.grid.get_neighbors(self.pos, moore=True, include_center=False):


   print(f"Checking tree at {neighbor.pos} with survival probability {neighbor.prob_de_sobrevivencia}")
                    random_value = self.random.random()
                    print(f"Generated random value: {random_value}")
                    # Se a probabilidade de sobrevivência for 1, a árvore não queima
                    if neighbor.prob_de_sobrevivencia == 1:
                        print(f"Tree at {neighbor.pos} has a survival probability of 1, it will not burn.")
                    # Se o valor aleatório for menor que a probabilidade de sobrevivência, a árvore sobrevive
                    elif random_value < neighbor.prob_de_sobrevivencia:
                        print(f"Tree at {neighbor.pos} survived the fire.")
                    else:
                        print(f"Tree at {neighbor.pos} burned due to random value exceeding survival probability.")


   else:
            print(f"Tree at {self.pos} is in state: {self.condition}")




## Update 5 - prob_de_sobrevivencia - model

- Segue abaixo a alteração feita no código


                new_tree = TreeCell((x, y), self, self.prob_de_sobrevivencia)











