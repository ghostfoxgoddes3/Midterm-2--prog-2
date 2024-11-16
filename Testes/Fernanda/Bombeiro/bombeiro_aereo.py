import mesa
from agent import TreeCell, Person

class AirFirefighter(Person):
    def __init__(self, pos, model, resistencia_fogo=1, resistencia_fumaca=1):
        super().__init__(pos, model)  # Chama o construtor da classe Person
        self.special_skill = "Firefighting"
        self.speed = 5
        self.resistencia_fogo = resistencia_fogo
        self.resistencia_fumaca = resistencia_fumaca

    def step(self):
        """Método para apagar fogo nas árvores próximas"""
        # Verifica se há fogo na célula atual
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
        current_cell = self.model.grid.get_cell_list_contents(self.pos)
        tree = next((obj for obj in current_cell if isinstance(obj, TreeCell)), None)

        for neighbor in neighbors:
            if isinstance(neighbor, TreeCell) and neighbor.condition == "On Fire":
                neighbor.condition = "Fire Off"

        # Se necessário, pode mover o bombeiro para a árvore em chamas mais próxima
        fire_positions = [
            (agent.pos, agent) for agent in self.model.schedule.agents
            if isinstance(agent, TreeCell) and agent.condition == "On Fire"
        ]
        if fire_positions:
            # Escolher a árvore em chamas mais próxima
            closest_fire = min(fire_positions, key=lambda f: ((self.pos[0] - f[0][0]) ** 2 + (self.pos[1] - f[0][1]) ** 2) ** 0.5)[0]
            self.model.grid.move_agent(self, closest_fire)