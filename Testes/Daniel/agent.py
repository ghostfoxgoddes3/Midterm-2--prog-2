import mesa
from collections import deque
import random


class TreeCell(mesa.Agent):
    def __init__(self, pos, model, prob_de_sobrevivencia=0):
        """
        Create a new tree with a given probability of survival.
        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
            prob_de_sobrevivencia: Probability of the tree surviving the fire.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Fine"
        self.prob_de_sobrevivencia = prob_de_sobrevivencia  # New attribute

    def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby with a chance of survival.
        """
        if self.condition == "On Fire":
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if neighbor.condition == "Fine":
                    # Check survival probability
                    if self.random.random() > neighbor.prob_de_sobrevivencia:
                        neighbor.condition = "On Fire"
            self.condition = "Burned Out"


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
            """
            modifiquei a condição antiga:
            if any([agent.condition == "On Fire" for agent in current_cell]):
            
            Durante os testes, identifiquei um comportamento inesperado na interação entre os agentes `Person` e `TreeCell`. 
            Se o método `step` da classe `Person` fosse executado antes do método `step` da classe `TreeCell`, 
            as árvores próximas não teriam atualizado sua condição para "On Fire", resultando em um cenário onde 
            a pessoa permanecia viva mesmo estando em uma área que deveria estar em chamas.

            Porém, se no próximo método `step` da classe `TreeCell` fosse executado primeiro, a árvore já poderia 
            ter sua condição atualizada para "Burned Out", e a pessoa novamente não seria afetada.

            Assim inclui a condição "Burned Out" também para garantimos que a pessoa possa ser afetada mesmo que a árvore no mesmo 
            espaço tenha progredido para a condição "Burned Out".
            """
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
    def __init__(self, pos, model, bomb_radius=3, speed=3, cooldown=3):
        super().__init__(pos, model)
        self.bomb_radius = bomb_radius  # Raio do bombardeio
        self.speed = speed  # Velocidade do Bombardeiro
        self.cooldown = cooldown  # Cooldown em número de passos
        self.steps_until_next_bombard = 0  # Contador de cooldown
        self.target_path = []  # Caminho até a próxima árvore saudável
        self.captured = False  # Marca o Bombardeiro como não capturado inicialmente

    def step(self):
        if self.captured:
            return  # Se o Bombardeiro foi capturado, ele não faz nada

        # Decrementa o contador de cooldown
        if self.steps_until_next_bombard > 0:
            self.steps_until_next_bombard -= 1

        # Se não tem caminho, encontra um novo caminho até a árvore saudável mais próxima
        if not self.target_path:
            self.target_path = self.find_path_to_healthy_tree(self.pos)
            if not self.target_path:
                # Fallback: Movimento aleatório
                neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
                if neighbors:  # Certifique-se de que existem vizinhos
                    random_move = random.choice(neighbors)
                    self.model.grid.move_agent(self, random_move)
                return

        # Se o caminho foi encontrado, move para o próximo passo
        if self.target_path:
            next_step = self.target_path.pop(0)
            self.model.grid.move_agent(self, next_step)

        # Realiza o bombardeio se o cooldown permitir
        if self.steps_until_next_bombard == 0:
            self.bombard_trees()
            self.steps_until_next_bombard = self.cooldown

    def find_path_to_healthy_tree(self, start_pos):
        """
        Busca em largura (BFS) para encontrar o menor caminho até uma árvore saudável.
        Permite passar por qualquer célula no grid, independentemente do conteúdo.
        """
        queue = deque([(start_pos, [])])  # Fila de posições a serem exploradas e o caminho até elas
        visited = set()  # Conjunto de posições visitadas

        while queue:
            current_pos, path = queue.popleft()

            # Evita revisitar células
            if current_pos in visited:
                continue
            visited.add(current_pos)

            # Verifica se há uma árvore saudável na célula atual
            current_cell = self.model.grid.get_cell_list_contents(current_pos)
            tree = next((obj for obj in current_cell if isinstance(obj, TreeCell) and obj.condition == "Fine"), None)

            if tree:  # Se encontrar uma árvore saudável
                return path + [current_pos]  # Retorna o caminho até a árvore saudável

            # Explora todos os vizinhos, permitindo atravessar qualquer célula
            neighbors = self.model.grid.get_neighborhood(current_pos, moore=False, include_center=False)
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, path + [current_pos]))

        return []  # Retorna caminho vazio se não encontrar árvore saudável

    def choose_random_path(self):
        """Escolhe um caminho aleatório entre as células vizinhas."""
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        random.shuffle(neighbors)  # Embaralha as células vizinhas para garantir aleatoriedade
        return neighbors  # Retorna as células vizinhas para o movimento aleatório

    def bombard_trees(self):
        """Bombardeia as árvores dentro do raio de ação."""
        trees_in_radius = [
            agent for agent in self.model.grid.get_neighbors(self.pos, moore=True, radius=self.bomb_radius)
            if isinstance(agent, TreeCell) and agent.condition == "Fine"
        ]
        for tree in trees_in_radius:
            tree.condition = "Toasted"  # Marca as árvores como "Toasted" para indicar que foram bombardeadas

class Logger(Person):
    """
    Representa o agente Logger (Madeireiro).
    O Logger pode cortar árvores ao seu redor dentro de um raio especificado.
    """
    def __init__(self, pos, model, cut_radius=2, cooldown=3):
        """
        Inicializa o Logger.

        Args:
            pos: Posição inicial do Logger no grid.
            model: Instância do modelo.
            cut_radius: Raio dentro do qual o Logger pode cortar as árvores.
            cooldown: Número de passos antes de poder cortar novamente.
        """
        super().__init__(pos, model)
        self.cut_radius = cut_radius  # Raio de corte de árvores
        self.captured = False  # Se o logger for capturado (pela polícia)
        self.target_path = []  # Caminho até a próxima árvore saudável
        self.cooldown = cooldown  # Número de passos entre cortes
        self.steps_until_next_cut = 0  # Contador de cooldown

    def step(self):
        """
        Executa a ação do Logger em cada passo.
        O Logger corta as árvores dentro do seu raio de ação.
        """
        if self.captured:
            return  # Se o Logger for capturado, ele não realiza mais ações.

        # Decrementa o cooldown
        if self.steps_until_next_cut > 0:
            self.steps_until_next_cut -= 1

        # Se não tem caminho, encontra um novo caminho até a árvore saudável mais próxima
        if not self.target_path:
            self.target_path = self.find_path_to_healthy_tree(self.pos)
            if not self.target_path:
                # Fallback: Movimento aleatório
                neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
                if neighbors:  # Certifique-se de que existem vizinhos
                    random_move = random.choice(neighbors)
                    self.model.grid.move_agent(self, random_move)
                return

        # Move para o próximo passo no caminho
        if self.target_path:
            next_step = self.target_path.pop(0)
            self.model.grid.move_agent(self, next_step)

        # Tenta cortar árvores se o cooldown permitir
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

    def find_path_to_healthy_tree(self, start_pos):
        """
        Busca em largura (BFS) para encontrar o menor caminho até uma árvore saudável.
        Permite passar por qualquer célula no grid, independentemente do conteúdo.
        """
        queue = deque([(start_pos, [])])  # Fila de posições a serem exploradas e o caminho até elas
        visited = set()  # Conjunto de posições visitadas

        while queue:
            current_pos, path = queue.popleft()

            # Evita revisitar células
            if current_pos in visited:
                continue
            visited.add(current_pos)

            # Verifica se há uma árvore saudável na célula atual
            current_cell = self.model.grid.get_cell_list_contents(current_pos)
            tree = next((obj for obj in current_cell if isinstance(obj, TreeCell) and obj.condition == "Fine"), None)

            if tree:  # Se encontrar uma árvore saudável
                return path + [current_pos]  # Retorna o caminho até a árvore saudável

            # Explora todos os vizinhos, permitindo atravessar qualquer célula
            neighbors = self.model.grid.get_neighborhood(current_pos, moore=False, include_center=False)
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, path + [current_pos]))

        return []  # Retorna caminho vazio se não encontrar árvore saudável
