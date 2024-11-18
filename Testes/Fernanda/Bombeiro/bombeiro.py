import mesa
from agent import TreeCell, Person
import random

class GroundFirefighter(Person):
    def __init__(self, pos, model, resistencia_fogo=1, resistencia_fumaca=1, search_radius=3):
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
