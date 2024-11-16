import mesa
import math
from agent import TreeCell, CityCell  # Importando as classes TreeCell e CityCell


class ForestFire(mesa.Model):
    """
    Modelo de incêndio florestal com árvores e cidades.
    """

    def __init__(self, width=100, height=100, density=0.65, prob_de_sobrevivencia=0.0, city_probability=0.01):
        """
        Cria um novo modelo de incêndio florestal com árvores e cidades.

        Args:
            width, height: O tamanho da grade para modelar
            density: A fração de células com árvores
            prob_de_sobrevivencia: A probabilidade de uma árvore sobreviver ao fogo
            city_probability: A probabilidade de uma célula ser uma cidade
        """
        super().__init__()

        # Configura objetos do modelo
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.prob_de_sobrevivencia = prob_de_sobrevivencia  # Probabilidade de sobrevivência das árvores

        self.datacollector = mesa.DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
                "Cities Evacuated": lambda m: self.count_type(m, "Evacuated"),  # Contando cidades evacuadas
            }
        )

        # Coloca árvores e cidades nas células
        for contents, (x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                # Cria uma árvore com a probabilidade de sobrevivência
                new_tree = TreeCell((x, y), self, self.prob_de_sobrevivencia)
                # Define todas as árvores da primeira coluna como "On Fire"
                if x == 0:
                    new_tree.condition = "On Fire"
                self.grid.place_agent(new_tree, (x, y))
                self.schedule.add(new_tree)

            # Cria cidades com base na probabilidade
            elif self.random.random() < city_probability:
                city = CityCell((x, y), self)
                self.grid.place_agent(city, (x, y))
                self.schedule.add(city)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Avança o modelo por um passo.
        """
        self.schedule.step()
        # Coleta dados
        self.datacollector.collect(self)

        # Interrompe se não houver mais fogo
        if self.count_type(self, "On Fire") == 0:
            self.running = False

    @staticmethod
    def count_type(model, condition):
        """
        Método auxiliar para contar agentes em uma dada condição no modelo.
        """
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, TreeCell) and agent.condition == condition:
                count += 1
            elif isinstance(agent, CityCell) and agent.condition == condition:
                count += 1
        return count
