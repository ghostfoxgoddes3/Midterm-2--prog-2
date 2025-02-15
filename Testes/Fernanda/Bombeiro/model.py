import mesa
import math
from agent import TreeCell, CityCell, GrassCell, Person, GroundFirefighter # Certifique-se de que GrassCell seja importado


class ForestFire(mesa.Model):
    def __init__(self, width=100, height=100, density=0.65, prob_de_sobrevivencia=0.0, vento="Norte", city_probability=0.01, grass_probability=0.05, num_pessoas=10):
        super().__init__()

        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.prob_de_sobrevivencia = prob_de_sobrevivencia
        self.vento = vento

        self.datacollector = mesa.DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
                "Cities Evacuated": lambda m: self.count_type(m, "Evacuated"),
                "Fire Off": lambda m: self.count_type(m, "Fire Off"),
            }
        )

        # Criando agentes no grid
        for contents, (x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                new_tree = TreeCell((x, y), self, self.prob_de_sobrevivencia)
                if x == 0:  # Vamos começar o fogo na posição (0, y)
                    new_tree.condition = "On Fire"
                self.grid.place_agent(new_tree, (x, y))
                self.schedule.add(new_tree)

            elif self.random.random() < city_probability:
                city = CityCell((x, y), self)
                self.grid.place_agent(city, (x, y))
                self.schedule.add(city)
            
            elif self.random.random() < grass_probability:  
                grass = GrassCell((x, y), self)
                self.grid.place_agent(grass, (x, y))
                self.schedule.add(grass)
        
        for _ in range(num_pessoas):
            x = self.random.randint(0, self.grid.height - 1)
            y = self.random.randint(0, self.grid.height - 1)
            new_person = GroundFirefighter((x, y), self)
            self.grid.place_agent(new_person, (x, y))
            self.schedule.add(new_person)

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
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, TreeCell) and agent.condition == condition:
                count += 1
            elif isinstance(agent, CityCell) and agent.condition == condition:
                count += 1
            elif isinstance(agent,GrassCell) and agent.condition == condition:
                count +=1
        return count


