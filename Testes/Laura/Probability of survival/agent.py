from mesa import Agent

class TreeCell(Agent):
    def __init__(self, pos, model, prob_de_sobrevivencia=0.5):
        super().__init__(pos, model)
        self.pos = pos
        self.model = model
        self.condition = "Fine"  # Possíveis condições: "Fine", "On Fire", "Burned Out"
        self.prob_de_sobrevivencia = prob_de_sobrevivencia

    def step(self):
        # Apenas espalha fogo se a árvore está pegando fogo
        if self.condition == "On Fire":
            print(f"Tree at {self.pos} is on fire, spreading fire to neighbors...")
            for neighbor in self.model.grid.get_neighbors(self.pos, moore=True, include_center=False):
                if neighbor.condition == "Fine":
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
                        neighbor.condition = "On Fire"
            self.condition = "Burned Out"
        else:
            print(f"Tree at {self.pos} is in state: {self.condition}")
