import mesa
import math

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
                if neighbor.condition == "Fine":
                    neighbor.condition = "On Fire"
            self.condition = "Burned Out"

        # Alerta de evacuação para as cidades dentro do raio de 10 células
        if self.condition == "City":
            # Verifica se o fogo está dentro do raio de 10 células
            for x in range(self.pos[0] - 10, self.pos[0] + 11):
                for y in range(self.pos[1] - 10, self.pos[1] + 11):
                    # Ignorar a célula da cidade ou fora dos limites
                    if (x, y) == self.pos or not self.model.grid.in_bounds((x, y)):
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
                                break
                if self.alert:
                    break





