import mesa
from agent import TreeCell

class ForestFire(mesa.Model):
    """
    Modelo simples de incêndio florestal.
    """

    def __init__(self, width=100, height=100, density=0.65, prob_de_sobrevivencia=0.5, vento="Norte"):
        """
        Cria um novo modelo de incêndio florestal.

        Args:
            width, height: Tamanho da grade.
            density: Fração de células com árvores.
            prob_de_sobrevivencia: Probabilidade de uma árvore sobreviver ao fogo.
            vento: Direção do vento que influencia a propagação ("Norte", "Sul", "Leste", "Oeste").
        """
        super().__init__()
        # Configura o modelo e define atributos
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.SingleGrid(width, height, torus=False)
        self.prob_de_sobrevivencia = prob_de_sobrevivencia
        self.vento = vento  # Define a direção do vento no modelo

        self.datacollector = mesa.DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
            }
        )

        # Posiciona uma árvore em cada célula com probabilidade definida por density
        for contents, (x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                # Cria uma nova árvore
                new_tree = TreeCell((x, y), self, prob_de_sobrevivencia=prob_de_sobrevivencia)
                # Define todas as árvores na primeira coluna como pegando fogo
                if x == 0:
                    new_tree.condition = "On Fire"
                self.grid.place_agent(new_tree, (x, y))
                self.schedule.add(new_tree)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Avança o modelo em um passo.
        """
        self.schedule.step()
        # Coleta dados
        self.datacollector.collect(self)

        # Para a simulação se não houver mais fogo
        if self.count_type(self, "On Fire") == 0:
            self.running = False

    @staticmethod
    def count_type(model, tree_condition):
        """
        Conta o número de árvores em uma condição específica.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count
