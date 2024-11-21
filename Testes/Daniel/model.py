import mesa
#from mesa.time import BaseScheduler
from agent import TreeCell, GroundFirefighter, Police, Incendiary

class ForestFire(mesa.Model):
    """
    Simple Forest Fire model.
    """

    def __init__(self, width=100, height=100, density=0.65, prob_de_sobrevivencia=0.5, num_policiais=5, num_incendiarios=3):
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
        self.prob_de_sobrevivencia = prob_de_sobrevivencia  # Adiciona a probabilidade de sobrevivência
        self.datacollector = mesa.DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
                "Fire Off": lambda m: self.count_type(m, "Fire Off"),
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
            
        # Coloca policiais no grid
        for _ in range(num_policiais):
            x = self.random.randint(0, self.grid.width - 1)
            y = self.random.randint(0, self.grid.height - 1)
            new_police = Police((x, y), self, range_view=3)
            self.grid.place_agent(new_police, (x, y))
            self.schedule.add(new_police)

        #Coloca incendiários no grid
        for _ in range(num_incendiarios):
            x = self.random.randint(0, self.grid.width - 1)
            y = self.random.randint(0, self.grid.height - 1)
            new_incendiary = Incendiary((x, y), self, chance_incendiar=0.4)
            self.grid.place_agent(new_incendiary, (x, y))
            self.schedule.add(new_incendiary)

        self.running = True
        self.datacollector.collect(self)

    def step(self): #, shuffle_types = False, shuffle_agents = False
        """
        Avança o modelo por um passo.
        """
        # Estive tendo problema na ativação da condição de vida da pessoa  morrer, 
        # porque se o step da pessoa ocorrer antes da arvore, não é encontrado fogo
        # naquele quadrante do grid, então a pessoa não morre
        # Para resolver isso, eu coloquei a arvore em primeiro lugar na lista de agent
        # Primeiro, ativa os agentes do tipo "TreeCell" (Árvores)
       
        '''
        # Primeiro, ativa os agentes do tipo "TreeCell" (Árvores)
        # Depois, ativa os agentes do tipo "Person" (Pessoas)

        self.schedule.step_type(TreeCell)
        
        self.schedule.step_type(Person)

        '''
        
        self.schedule.step()
        # Coleta os dados para análise
        self.datacollector.collect(self)

        # Se não há mais árvores pegando fogo, a simulação é parada
        if self.count_type(self, "On Fire") == 0:
            self.running = False


    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count
