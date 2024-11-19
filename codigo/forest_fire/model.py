import mesa
import math
from agent import TreeCell, CityCell  # Importando as classes TreeCell e CityCell

class ForestFire(mesa.Model):
    """
    Modelo de incêndio florestal com árvores e cidades.
    """

    def __init__(self, width=100, height=100, density=0.65, prob_de_sobrevivencia=0.0, vento="Norte", city_probability=0.01):
        """
        Cria um novo modelo de incêndio florestal com árvores e cidades.

        Args:
            width, height: O tamanho da grade para modelar
            density: A fração de células com árvores
            prob_de_sobrevivencia: A probabilidade de uma árvore sobreviver ao fogo
            vento: A direção do vento (Norte, Sul, Leste, Oeste)
            city_probability: A probabilidade de uma célula ser uma cidade
        """
        super().__init__()

        # Configura objetos do modelo
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.prob_de_sobrevivencia = prob_de_sobrevivencia  # Probabilidade de sobrevivência das árvores
        self.vento = vento  # Direção do vento no modelo

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
                new_tree = TreeCell((x, y), self, self.prob_de_sobrevivencia, vento=self.vento)
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

# Definição de TreeCell
class TreeCell(mesa.Agent):
    def __init__(self, pos, model, prob_de_sobrevivencia, vento="Norte"):
        """
        Cria uma nova árvore com uma dada probabilidade de sobrevivência.

        Args:
            pos: Coordenadas da árvore na grade.
            model: Referência do modelo padrão para o agente.
            prob_de_sobrevivencia: Probabilidade de a árvore sobreviver ao fogo.
            vento: Direção do vento que afeta a propagação do fogo.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Fine"
        self.prob_de_sobrevivencia = prob_de_sobrevivencia
        self.vento = vento  # Direção do vento

    def ajusta_probabilidade_por_vento(self, neighbor_pos):
        """
        Ajusta a probabilidade de sobrevivência com base na direção do vento.
        
        Args:
            neighbor_pos: A posição do vizinho.
            
        Returns:
            nova_probabilidade: A probabilidade ajustada considerando o vento.
        """
        if self.model.vento == "Sem Direção":
            return self.prob_de_sobrevivencia  # Sem alteração na probabilidade se o vento não tiver direção
        
        # Define um aumento da chance de pegar fogo se o vento estiver na direção certa
        incremento_vento = 0.5
        if self.model.vento == "Norte":
            incremento_vento = 0.7
        elif self.model.vento == "Sul":
            incremento_vento = 0.7
        elif self.model.vento == "Leste" or self.model.vento == "Oeste":
            incremento_vento = 0.5

        # Calcular a direção do vento e ajustar a probabilidade de pegar fogo
        if self.model.vento == "Norte" and neighbor_pos[1] < self.pos[1]:  # Vento vindo do Norte
            return max(0, self.prob_de_sobrevivencia - incremento_vento)
        elif self.model.vento == "Sul" and neighbor_pos[1] > self.pos[1]:  # Vento vindo do Sul
            return max(0, self.prob_de_sobrevivencia - incremento_vento)
        elif self.model.vento == "Leste" and neighbor_pos[0] < self.pos[0]:  # Vento vindo do Leste
            return max(0, self.prob_de_sobrevivencia - incremento_vento)
        elif self.model.vento == "Oeste" and neighbor_pos[0] > self.pos[0]:  # Vento vindo do Oeste
            return max(0, self.prob_de_sobrevivencia - incremento_vento)

        # Se o vento não está na direção certa, a probabilidade de sobrevivência não é ajustada
        return self.prob_de_sobrevivencia

    def step(self):
        """
        Se a árvore estiver pegando fogo, espalha-o para árvores próximas, considerando o vento.
        """
        if self.condition == "On Fire":
            for neighbor in self.model.grid.get_neighbors(self.pos, moore=True, include_center=False):
                if neighbor.condition == "Fine":
                    # Ajustar a probabilidade com base no vento
                    probabilidade_ajustada = neighbor.ajusta_probabilidade_por_vento(self.pos)
                    
                    # Verificar probabilidade ajustada para pegar fogo
                    if self.random.random() > probabilidade_ajustada:
                        neighbor.condition = "On Fire"
            # Alterar a condição da árvore para "Burned Out"
            self.condition = "Burned Out"
