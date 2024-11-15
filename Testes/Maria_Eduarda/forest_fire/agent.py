import mesa

#Testando mudanças com o código da Laura
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




       




