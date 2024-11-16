import mesa
import math


class TreeCell(mesa.Agent):
    """
    A tree in the forest.
    """

    def __init__(self, pos, model, prob_de_sobrevivencia):
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

    def in_bounds(self, pos): #ADICIONAR COMENTARIO DO PQ DESSA FUNÇÃO
        x, y = pos
        # Verificar se as coordenadas estão dentro dos limites da grade
        return 0 <= x < self.model.grid.width and 0 <= y < self.model.grid.height




class CityCell(mesa.Agent):
    """
    A city in the forest.
    """

    def __init__(self, pos, model, condition = "City"):
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "City"  # Condições possíveis: "City", "Evacuated"
        self.alert = False  # Flag para indicar o alerta de evacuação

    def step(self):
        # Alerta de evacuação para as cidades dentro do raio de 10 células
        if self.condition == "City":
            for x in range(self.pos[0] - 10, self.pos[0] + 11):
                for y in range(self.pos[1] - 10, self.pos[1] + 11):
                    # Ignorar a célula da cidade ou fora dos limites
                    if (x, y) == self.pos or not (0 <= x < self.model.grid.width and 0 <= y < self.model.grid.height):
                        continue
                    # Calcular a distância entre as células
                    distance = math.sqrt((self.pos[0] - x) ** 2 + (self.pos[1] - y) ** 2)
                    # Se o fogo está dentro do raio e encontrou uma célula em chamas, evacuar
                    if distance <= 10:
                        neighbor = self.model.grid.get_cell_list_contents([(x, y)])
                        for n in neighbor:
                            if n.condition == "On Fire":
                                self.alert = True
                                self.condition = "Evacuated"  # Evacuar a cidade
                                return

    def in_bounds(self, pos):
        x, y = pos
        # Verificar se as coordenadas estão dentro dos limites da grade
        return 0 <= x < self.model.grid.width and 0 <= y < self.model.grid.height
