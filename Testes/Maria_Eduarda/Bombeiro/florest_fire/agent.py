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
        """Espalha o fogo para as árvores vizinhas."""
        if self.condition == "Fire Off":
            # Se o fogo foi apagado, a árvore não espalha mais fogo.
            return

        elif self.condition == "On Fire":
            # Espalha o fogo para vizinhos
            for neighbor in self.model.grid.iter_neighbors(self.pos, moore=True, include_center=False):
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
         
from collections import deque

class GroundFirefighter(Person):
    def __init__(self, pos, model, resistencia_fogo=1, resistencia_fumaca=1):
        super().__init__(pos, model)  # Chama o construtor da classe Person
        self.special_skill = "Firefighting"
        self.speed = 1
        self.resistencia_fogo = resistencia_fogo
        self.resistencia_fumaca = resistencia_fumaca
        self.target_path = []  # Caminho até o próximo fogo

    def step(self):
        current_cell = self.model.grid.get_cell_list_contents(self.pos)
        tree = next((obj for obj in current_cell if isinstance(obj, TreeCell)), None)

        if tree and (tree.condition == "On Fire" or tree.condition == "Burned Out"):
            tree.condition = "Fire Off" # Apaga o fogo
            self.target_path = []  # Limpa o caminho após apagar o fogo
        elif not self.target_path:
            # Se não tem caminho, encontra um novo caminho até o fogo
            self.target_path = self.find_path_to_fire(self.pos)
        if self.target_path:
            # Move para o próximo passo no caminho
            next_step = self.target_path.pop(0)
            self.model.grid.move_agent(self, next_step)

    def find_path_to_fire(self, start_pos):
        """Busca em largura (BFS) para encontrar o menor caminho até uma célula com fogo."""
        queue = deque([(start_pos, [])])  # Fila de posições a serem exploradas e o caminho até elas
        visited = set()  # Conjunto de posições visitadas

        while queue:
            current_pos, path = queue.popleft()

            # Evita revisitar células
            if current_pos in visited:
                continue
            visited.add(current_pos)

            current_cell = self.model.grid.get_cell_list_contents(current_pos)
            tree = next((obj for obj in current_cell if isinstance(obj, TreeCell)), None)

            if tree and tree.condition == "On Fire":
                return path + [current_pos]  # Retorna o caminho até a célula com fogo

            # Explora os vizinhos ortogonais
            neighbors = self.model.grid.get_neighborhood(current_pos, moore=False, include_center=False)
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, path + [current_pos]))

        return []  # Retorna caminho vazio se não encontrar fogo


