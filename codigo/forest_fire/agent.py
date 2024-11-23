import mesa
import math
import random
from collections import deque


class TreeCell(mesa.Agent):
    """
    A tree in the forest.
    A árvore da floresta, com a probabilidade de sobrevivência e influência do vento.
    """

    def __init__(self, pos, model, prob_de_sobrevivencia):
        """
        Cria uma nova árvore com uma dada probabilidade de sobrevivência.
        Args:
            pos: Coordenadas da árvore na grade.
            model: Referência do modelo padrão para o agente.
            prob_de_sobrevivencia: Probabilidade de a árvore sobreviver ao fogo.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.model = model
        self.condition = "Fine"  # Possíveis condições: "Fine", "On Fire", "Burned Out"
        self.prob_de_sobrevivencia = prob_de_sobrevivencia  # Atributo de probabilidade de sobrevivência

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
        if self.model.vento in ["Norte", "Sul"]:
            incremento_vento = 0.7
        else:
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
                    random_value = self.random.random()

                    if random_value > probabilidade_ajustada:
                        neighbor.condition = "On Fire"
            # Alterar a condição da árvore para "Burned Out"
            self.condition = "Burned Out"
        else:
            print(f"Tree at {self.pos} is in state: {self.condition}")

    def in_bounds(self, pos):
        """
        Verifica se a posição fornecida está dentro dos limites da grade.
        """
        x, y = pos
        return 0 <= x < self.model.grid.width and 0 <= y < self.model.grid.height


class CityCell(mesa.Agent):
    """
    A cidade na floresta, com alerta de evacuação baseado no fogo.
    """

    def __init__(self, pos, model, condition="City"):
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "City"  # Condições possíveis: "City", "Evacuated"
        self.alert = False  # Flag para indicar o alerta de evacuação

    def step(self):
        # Alerta de evacuação para as cidades dentro do raio de 10 células
        if self.condition == "City":
            for x in range(self.pos[0] - 10, self.pos[0] + 11):
                for y in range(self.pos[1] - 10, self.pos[1] + 11):
                    # Ignorar a célula da cidade ou fora dos limites
                    if (x, y) == self.pos or not (0 <= x < self.model.grid.width and 0 <= y < self.model.grid.height):
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
                                return

    def in_bounds(self, pos):
        """
        Verifica se a posição fornecida está dentro dos limites da grade.
        """
        x, y = pos
        return 0 <= x < self.model.grid.width and 0 <= y < self.model.grid.height

class GrassCell(mesa.Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Fine"  # "Fine", "On Fire", "Burned Out"

    def ajusta_probabilidade_por_vento(self, neighbor_pos):
        #funçao nao utilizada diretamente, apenas para o codigo rodar        
        return 0.1
    def step(self):
            if self.condition == "On Fire":
                for neighbor in self.model.grid.get_neighbors(self.pos, moore=True, include_center=False):
                    if neighbor.condition == "Fine" :
                        if self.random.random() < 0.15:    #prob. arbitraria para queimar os vizinhos
                            neighbor.condition = "On Fire"
                self.condition = "Burned Out"

class Person(mesa.Agent):
    """Classe base para as pessoas na simulação."""
    def __init__(self, pos, model, resistencia_fogo=0, resistencia_fumaca=0.5):
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Alive"
        self.fire_resistance = resistencia_fogo
        self.smoke_resistance = resistencia_fumaca

    def step(self):
        """Atualiza o estado da pessoa, verificando os perigos do fogo."""
        if self.condition == "Alive":
            current_cell = self.model.grid.get_cell_list_contents([self.pos])

            # Verifica se a célula atual tem fogo
            if any(agent.condition in ["On Fire", "Burned Out"] for agent in current_cell):
                if self.random.random() > self.fire_resistance:
                    self.condition = "Dead"
                    return

            # Verifica os vizinhos para risco de fumaça
            for neighbor in self.model.grid.iter_neighbors(self.pos, moore=True):
                if isinstance(neighbor, TreeCell) and neighbor.condition == "On Fire":
                    if self.random.random() > self.smoke_resistance:
                        self.condition = "Dead"
                        break


class GroundFirefighter(Person):
    """Representa um bombeiro terrestre."""
    def __init__(self, pos, model, resistencia_fogo=1, resistencia_fumaca=1):
        super().__init__(pos, model, resistencia_fogo, resistencia_fumaca)

    def find_path_to_fire(self, start_pos):
        """Busca em largura (BFS) para encontrar o menor caminho até o fogo."""
        queue = deque([start_pos])  # Fila de posições a explorar
        visited = set()  # Conjunto de posições visitadas

        while queue:
            current_pos = queue.popleft()
            if current_pos in visited:
                continue
            visited.add(current_pos)

            # Verifica os agentes na célula
            cell_contents = self.model.grid.get_cell_list_contents([current_pos])
            if any(isinstance(agent, TreeCell) and agent.condition == "On Fire" for agent in cell_contents):
                return current_pos

            # Adiciona vizinhos à fila
            neighbors = self.model.grid.get_neighborhood(current_pos, moore=True, include_center=False)
            queue.extend(neighbor for neighbor in neighbors if neighbor not in visited)

        return None  # Retorna None se nenhum fogo for encontrado

    def step(self):
        """Move o bombeiro em direção ao fogo e apaga-o se estiver na mesma célula."""
        # Atualiza ou encontra o caminho até o fogo
       
        self.target_pos = self.find_path_to_fire(self.pos)

        # Move-se passo a passo em direção ao alvo
        if self.target_pos:
            x, y = self.pos
            x_ALVO, y_ALVO = self.target_pos

            # Calcula o deslocamento horizontal e vertical
            new_x = x + (1 if x_ALVO > x else -1 if x_ALVO < x else 0)
            new_y = y + (1 if y_ALVO > y else -1 if y_ALVO < y else 0)
            nova_pos = (new_x, new_y)

            # Move o agente se a nova posição estiver dentro do grid
            if not self.model.grid.out_of_bounds(nova_pos):
                self.model.grid.move_agent(self, nova_pos)

            # Se chegou no alvo, reseta o alvo
            '''if nova_pos == self.target_pos:
                self.target_pos = None'''

        # Verifica e apaga o fogo na célula atual
        current_cell = self.model.grid.get_cell_list_contents([self.pos])
        tree = next((obj for obj in current_cell if isinstance(obj, TreeCell)), None)

        if tree and tree.condition == "On Fire":
            tree.condition = "Fire Off"  # Apaga o fogo
            self.target_pos = None  # Reseta o alvo após apagar o fogo

class AerialFirefighter(mesa.Agent):
    """Representa um bombeiro aéreo que se move rapidamente e apaga o fogo na célula atual e vizinhas."""

    def __init__(self, pos, model, velocidade=3):
        """
        Cria um bombeiro aéreo.
        Args:
            pos: Posição inicial do bombeiro.
            model: Referência ao modelo.
            velocidade: Velocidade de movimentação do bombeiro aéreo.
        """
        super().__init__(pos, model)
        self.velocidade = velocidade  # Velocidade de movimentação
        self.condition = "Aerial"          # Tipo do agente (bombeiro aéreo)

    def apagar_fogo(self, pos):
        """
        Apaga o fogo na célula atual e nas vizinhas.
        Args:
            pos: Posição central para apagar o fogo.
        """
        # Obtém todas as células na vizinhança de Moore (8 vizinhos) + a posição atual
        area_alvo = self.model.grid.get_neighborhood(pos, moore=True, include_center=True)
        for cell in area_alvo:
            cell_contents = self.model.grid.get_cell_list_contents([cell])
            for agent in cell_contents:
                if isinstance(agent, TreeCell) and agent.condition == "On Fire":
                    agent.condition = "Fire Off"  # Apaga o fogo

    def find_path_to_fire(self, start_pos):
        """
        Busca em largura (BFS) para encontrar o menor caminho até o fogo.
        Args:
            start_pos: Posição inicial do bombeiro.
        Returns:
            A posição de uma célula com fogo ou `None` se não houver fogo.
        """
        queue = deque([start_pos])  # Fila de posições a explorar
        visited = set()            # Conjunto de posições visitadas

        while queue:
            current_pos = queue.popleft()
            if current_pos in visited:
                continue
            visited.add(current_pos)

            # Verifica os agentes na célula
            cell_contents = self.model.grid.get_cell_list_contents([current_pos])
            if any(isinstance(agent, TreeCell) and agent.condition == "On Fire" for agent in cell_contents):
                return current_pos

            # Adiciona vizinhos à fila
            neighbors = self.model.grid.get_neighborhood(current_pos, moore=True, include_center=False)
            queue.extend(neighbor for neighbor in neighbors if neighbor not in visited)

        return None  # Retorna None se nenhum fogo for encontrado

    def step(self):
        """
        Move o bombeiro em direção ao fogo e apaga-o, incluindo as células vizinhas.
        """
        # Atualiza ou encontra o caminho até o fogo
        self.target_pos = self.find_path_to_fire(self.pos)

        if self.target_pos:
            x, y = self.pos
            x_alvo, y_alvo = self.target_pos

            # Calcula o deslocamento horizontal e vertical com base na velocidade
            new_x = x + self.velocidade * (1 if x_alvo > x else -1 if x_alvo < x else 0)
            new_y = y + self.velocidade * (1 if y_alvo > y else -1 if y_alvo < y else 0)
            nova_pos = (new_x, new_y)

            # Move o agente se a nova posição estiver dentro do grid
            if not self.model.grid.out_of_bounds(nova_pos):
                self.model.grid.move_agent(self, nova_pos)

            # Se atingir o alvo, apaga o fogo
            if nova_pos == self.target_pos:
                self.apagar_fogo(nova_pos)
                self.target_pos = None  # Reseta o alvo após apagar o fogo

        # Apaga fogo na célula atual e vizinhas se não estiver em movimento
        self.apagar_fogo(self.pos)
