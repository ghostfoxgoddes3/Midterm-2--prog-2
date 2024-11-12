import mesa
from agent import TreeCell

class GroundFirefighter(mesa.Agent):
    """O bombeiro que apaga o fogo"""
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos

    def step(self):
        """Apaga o fogo das árvores próximas"""
        # Verifica se há fogo na célula atual
        current_cell = self.model.grid.get_cell_list_contents(self.pos)
        tree = next((obj for obj in current_cell if isinstance(obj, TreeCell)), None)

        if tree and tree.condition == "On Fire":
            # Se há fogo na árvore, apaga
            tree.condition = "Fire Off"
        else:
            # Mover em direção à árvore em chamas mais próxima
            fire_positions = [
                (agent.pos, agent) for agent in self.model.schedule.agents
                if isinstance(agent, TreeCell) and agent.condition == "On Fire"
            ]
            if fire_positions:
                # Escolher a árvore em chamas mais próxima
                closest_fire = min(fire_positions, key=lambda f: ((self.pos[0] - f[0][0]) ** 2 + (self.pos[1] - f[0][1]) ** 2) ** 0.5)[0]
                self.model.grid.move_agent(self, closest_fire)
