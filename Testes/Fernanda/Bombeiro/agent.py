import mesa
import random

class TreeCell(mesa.Agent):
    """
    A tree cell.
    """
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Fine"  # O estado inicial da árvore é 'Fine'

    def step(self):
        """Espalha o fogo para as árvores vizinhas"""
        if self.condition == "On Fire":
            # Espalha o fogo para vizinhos
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if isinstance(neighbor, TreeCell) and neighbor.condition == "Fine":
                    neighbor.condition = "On Fire"  # Torna o vizinho em chamas
            self.condition = "Burned Out"  # A árvore que pegou fogo se queima

class Person(mesa.Agent):
    #Classe para as pessoas envolvidas na simulação
    def __init__(self, pos, model, resistencia_fogo = 0, resistencia_fumaca = 0.5):
        """
        Cria pessoas
        Args:
            pos: coordenada atual da pessoa no grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Alive" #condição viva ou morta
        self.speed = 1  # Velocidade da pessoa
        self.fire_resistance = resistencia_fogo  # Resistência da pessoa ao fogo
        self.smoke_resistance = resistencia_fumaca  # Resistência da pessoa aa fumaça (fogo em áreas vizinhas)

    def step(self):
        """
        Se a pessoa está numa área que está pegando fogo, ela pode morrer.
        """

        if self.condition == "Alive":
            #self.condition = "Dead"
            # Verificando se a própria posição da pessoa está pegando fogo
            current_cell = self.model.grid.get_cell_list_contents([self.pos])

            if any([agent.condition == "On Fire" or agent.condition == "Burned Out" for agent in current_cell]): #True
                    if self.fire_resistance == 0:
                        self.condition = "Dead"
                    # Check survival probability
                    if self.random.random() > self.fire_resistance: # Se a pessoa não sobrevive ao fogo
                        self.condition = "Dead" #morreu
                        return #não precisa continuar executando o método
                    #Se não caiu no IF anterior, é porque está viva e reperte o loop

            # Verificando os vizinhos da pessoa (onde o fogo pode se espalhar)
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if neighbor.condition == "On Fire":
                    # Verificar se a pessoa morre ou sobrevive ao fogo
                    if self.random.random() > self.smoke_resistance:
                        self.condition = "Dead"  # A pessoa morre
                        break  # Não precisa continuar verificando
         
class GroundFirefighter(Person):
    def __init__(self, pos, model, resistencia_fogo=1, resistencia_fumaca=1, search_radius=25):
        super().__init__(pos, model)  # Chama o construtor da classe Person
        self.special_skill = "Firefighting"
        self.speed = 1
        self.resistencia_fogo = resistencia_fogo
        self.resistencia_fumaca = resistencia_fumaca
        self.search_radius = search_radius  # Raio de detecção do fogo
        self.visited_positions = set()  # Armazena posições visitadas recentemente

    def step(self):
        # Verifica se há fogo na célula atual
        current_cell = self.model.grid.get_cell_list_contents(self.pos)
        tree = next((obj for obj in current_cell if isinstance(obj, TreeCell)), None)

        if tree and tree.condition == "On Fire":
            # Se há fogo na árvore, apaga
            tree.condition = "Fire Off"
        else:
            # Lista todas as árvores em chamas
            fire_positions = [
                (agent.pos, agent) for agent in self.model.schedule.agents
                if isinstance(agent, TreeCell) and agent.condition == "On Fire"
            ]

            # Verifica se há árvores em chamas próximas (dentro do raio de busca)
            close_fires = [
                (pos, agent) for pos, agent in fire_positions
                if ((self.pos[0] - pos[0]) ** 2 + (self.pos[1] - pos[1]) ** 2) ** 0.5 <= self.search_radius
            ]

            if close_fires:
                # Se há fogo próximo, move em direção à árvore em chamas mais próxima
                closest_fire = min(close_fires, key=lambda f: ((self.pos[0] - f[0][0]) ** 2 + (self.pos[1] - f[0][1]) ** 2) ** 0.5)[0]
                self.model.grid.move_agent(self, closest_fire)
            else:
                # Movimento mais diversificado
                self.explore_randomly()

    def explore_randomly(self):
        """Move aleatoriamente, mas evita áreas já exploradas."""
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        # Filtra posições já visitadas
        unexplored_steps = [pos for pos in possible_steps if pos not in self.visited_positions]

        if unexplored_steps:
            new_position = random.choice(unexplored_steps)
        else:
            # Se todos os vizinhos já foram explorados, escolhe aleatoriamente
            new_position = random.choice(possible_steps)

        # Adiciona a nova posição à lista de visitados
        self.visited_positions.add(new_position)
        # Limita o tamanho da memória
        if len(self.visited_positions) > 100:
            self.visited_positions.pop()

        # Move para a nova posição
        self.model.grid.move_agent(self, new_position)
