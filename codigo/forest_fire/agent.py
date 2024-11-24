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
class Police(Person):
    """
    Representa o agente Police (Policial).
    A Police captura Loggers ou Bombardeiros dentro de seu raio de visão.
    """
    def __init__(self, pos, model, range_view=3, speed=2):
        """
        Inicializa o Police.

        Args:
            pos: Posição inicial do Police no grid.
            model: Instância do modelo.
            range_view: Raio de visão dentro do qual pode capturar alvos.
            speed: Número de células que pode percorrer por passo.
        """
        super().__init__(pos, model)
        self.range_view = range_view  # Raio de visão para capturar alvos
        self.speed = speed  # Velocidade de movimento (células por passo)
        self.target_path = []  # Caminho até o próximo Bombardeiro ou Logger

    def step(self):
        """
        Executa a ação do Police em cada passo.
        O Police se move em direção ao alvo mais próximo (Logger ou Bombardeiro) e tenta capturá-lo.
        """
        if not self.target_path:
            # Se não tem caminho, encontra um novo caminho até o alvo mais próximo (Bombardeiro ou Logger)
            self.target_path = self.find_path_to_target(self.pos)
        
        if self.target_path:
            # Move para o próximo passo no caminho
            next_step = self.target_path.pop(0)
            self.model.grid.move_agent(self, next_step)

        # Verifica se está dentro do raio de visão de um Bombardeiro ou Logger
        for agent in self.model.grid.get_cell_list_contents(self.pos):
            if isinstance(agent, (Bomber, Logger)) and not agent.captured:  # Verifica se o alvo não foi capturado
                distance_to_target = self.distance(self.pos, agent.pos)
                if distance_to_target <= self.range_view:  # Captura o alvo se estiver dentro do raio de visão
                    agent.captured = True  # Marca o alvo como capturado
                    break  # Após capturar, não precisa verificar mais

    def find_path_to_target(self, start_pos):
        """
        Busca em largura (BFS) para encontrar o menor caminho até um Bombardeiro ou Logger.

        Args:
            start_pos: Posição inicial para iniciar a busca.

        Returns:
            Uma lista de posições representando o caminho até o alvo mais próximo,
            ou uma lista vazia se não houver alvos disponíveis.
        """
        queue = deque([(start_pos, [])])  # Fila de posições a serem exploradas e o caminho até elas
        visited = set()  # Conjunto de posições visitadas

        while queue:
            current_pos, path = queue.popleft()

            # Evita revisitar células
            if current_pos in visited:
                continue
            visited.add(current_pos)

            current_cell = self.model.grid.get_cell_list_contents(current_pos)
            # Verifica se há um Bombardeiro ou Logger
            target = next((obj for obj in current_cell if isinstance(obj, (Bomber, Logger)) and not obj.captured), None)

            if target:
                return path + [current_pos]  # Retorna o caminho até o alvo (Bombardeiro ou Logger)

            # Explora os vizinhos ortogonais
            neighbors = self.model.grid.get_neighborhood(current_pos, moore=False, include_center=False)
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, path + [current_pos]))

        return []  # Retorna caminho vazio se não encontrar nenhum alvo

    @staticmethod
    def distance(pos1, pos2):
        """
        Calcula a distância euclidiana entre duas posições.

        Args:
            pos1: Primeira posição (x, y).
            pos2: Segunda posição (x, y).

        Returns:
            Distância euclidiana entre as duas posições.
        """
        x1, y1 = pos1
        x2, y2 = pos2
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


class Bomber(Person):
    def __init__(self, pos, model, bomb_radius=3, speed=1, cooldown=5):
        super().__init__(pos, model)
        self.bomb_radius = bomb_radius  # Raio do bombardeio
        self.speed = speed  # Velocidade do Bombardeiro
        self.cooldown = cooldown  # Cooldown em número de passos
        self.steps_until_next_bombard = 0  # Contador de cooldown
        self.captured = False  # Marca o Bombardeiro como não capturado inicialmente

    def step(self):
        if self.captured:
            return  # Se o Bombardeiro foi capturado, ele não faz nada

        # Decrementa o contador de cooldown
        if self.steps_until_next_bombard > 0:
            self.steps_until_next_bombard -= 1

        # Movimento aleatório
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        if neighbors:
            new_pos = random.choice(neighbors)
            if not self.model.grid.out_of_bounds(new_pos):
                self.model.grid.move_agent(self, new_pos)

        # Bombardeia árvores se o cooldown permitir
        if self.steps_until_next_bombard == 0:
            self.bombard_trees()
            self.steps_until_next_bombard = self.cooldown  # Reseta o cooldown após bombardeio

    def bombard_trees(self):
        """Bombardeia as árvores dentro do raio de ação."""
        trees_in_radius = [
            agent for agent in self.model.grid.get_neighbors(self.pos, moore=True, radius=self.bomb_radius)
            if isinstance(agent, TreeCell) and agent.condition == "Fine"
        ]
        for tree in trees_in_radius:
            tree.condition = "Toasted"  # Marca as árvores como "Toasted" para indicar que foram bombardeadas


class Logger(Person):
    def __init__(self, pos, model, cut_radius=2, cooldown=3):
        super().__init__(pos, model)
        self.cut_radius = cut_radius  # Raio de corte de árvores
        self.captured = False  # Se o Logger foi capturado (pela polícia)
        self.cooldown = cooldown  # Número de passos entre cortes
        self.steps_until_next_cut = 0  # Contador de cooldown

    def step(self):
        if self.captured:
            return  # Se o Logger foi capturado, ele não realiza mais ações.

        # Decrementa o cooldown
        if self.steps_until_next_cut > 0:
            self.steps_until_next_cut -= 1

        # Movimento aleatório
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        if neighbors:
            new_pos = random.choice(neighbors)
            if not self.model.grid.out_of_bounds(new_pos):
                self.model.grid.move_agent(self, new_pos)

        # Corta árvores se o cooldown permitir
        if self.steps_until_next_cut == 0:
            self.cut_trees()
            self.steps_until_next_cut = self.cooldown  # Reseta o cooldown após cortar

    def cut_trees(self):
        """Corta as árvores dentro do raio de ação do Logger."""
        trees_in_radius = [
            agent for agent in self.model.grid.get_neighbors(self.pos, moore=True, radius=self.cut_radius)
            if isinstance(agent, TreeCell) and agent.condition == "Fine"
        ]
        for tree in trees_in_radius:
            tree.condition = "Blank"  # Marca a árvore como cortada ou queimada