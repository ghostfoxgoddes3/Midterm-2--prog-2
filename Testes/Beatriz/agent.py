class TreeCell(mesa.Agent):
    # Definição da classe TreeCell, que representa uma árvore no modelo de simulação.
    def __init__(self, pos, model, prob_de_sobrevivencia=0.5):
        """
        Cria uma nova árvore com uma dada probabilidade de sobrevivência.
        Args:
            pos: Coordenadas da árvore na grade (onde a árvore está localizada).
            model: Referência do modelo padrão para o agente (informações do ambiente).
            prob_de_sobrevivencia: Probabilidade de a árvore sobreviver ao fogo. 
        """
        super().__init__(pos, model)
        self.pos = pos  # Posição da árvore na grade.
        self.condition = "Fine"  # Condição inicial da árvore (sã e salva).
        self.prob_de_sobrevivencia = prob_de_sobrevivencia  # Probabilidade de sobrevivência da árvore.

    def ajusta_probabilidade_por_vento(self, neighbor_pos):
        """
        Ajusta a probabilidade de a árvore pegar fogo com base na direção do vento.
        
        O vento pode aumentar a chance de uma árvore pegar fogo dependendo da direção dele em relação 
        à posição da árvore. O vento pode vir de uma direção (Norte, Sul, Leste ou Oeste) e isso 
        pode afetar a árvore de acordo com sua posição em relação à vizinhança.
        
        Args:
            neighbor_pos: Posição do vizinho (ou seja, a posição da árvore adjacente).
        
        Returns:
            nova_probabilidade: A probabilidade ajustada de uma árvore sobreviver ao fogo 
            considerando o efeito do vento.
        """
        # Define um incremento que aumenta a chance de a árvore pegar fogo dependendo do vento
        incremento_vento = 0.2  # Aumenta a chance em 20% de pegar fogo quando o vento está na direção certa

        #  verifica a direção do vento e a posição do vizinho (a árvore adjacente)
        # O vento influencia a árvore quando a direção do vento está "a favor" da árvore pegar fogo.
        if self.model.vento == "Norte" and neighbor_pos[1] < self.pos[1]:  # Vento vindo do Norte
            # Se o vento vem do Norte e o vizinho está abaixo (na direção do vento), a árvore tem menos chance de sobreviver.
            return max(0, self.prob_de_sobrevivencia - incremento_vento)
        elif self.model.vento == "Sul" and neighbor_pos[1] > self.pos[1]:  # Vento vindo do Sul
            # Se o vento vem do Sul e o vizinho está acima, a probabilidade de sobrevivência é ajustada.
            return max(0, self.prob_de_sobrevivencia - incremento_vento)
        elif self.model.vento == "Leste" and neighbor_pos[0] > self.pos[0]:  # Vento vindo do Leste
            # Se o vento vem do Leste e o vizinho está à direita, a probabilidade de sobreviver diminui.
            return max(0, self.prob_de_sobrevivencia - incremento_vento)
        elif self.model.vento == "Oeste" and neighbor_pos[0] < self.pos[0]:  # Vento vindo do Oeste
            # Se o vento vem do Oeste e o vizinho está à esquerda, a chance de sobreviver também diminui.
            return max(0, self.prob_de_sobrevivencia - incremento_vento)
        
        # Caso o vento não esteja "a favor" do fogo (não está na direção certa), 
        # a probabilidade de sobrevivência não é alterada.
        return self.prob_de_sobrevivencia

    def step(self):
        """
        Se a árvore estiver pegando fogo, ela tenta espalhar o fogo para as árvores vizinhas,
        considerando a direção do vento.
        """
        if self.condition == "On Fire":  # Se a árvore está em chamas...
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):  # Para cada vizinho da árvore
                if neighbor.condition == "Fine":  # Se o vizinho está saudável (não pegando fogo)
                    # Ajusta a probabilidade de o vizinho pegar fogo, levando em conta a direção do vento
                    probabilidade_ajustada = neighbor.ajusta_probabilidade_por_vento(self.pos)
                    
                    # Verifica se o vizinho vai pegar fogo com base na probabilidade ajustada
                    if self.random.random() > probabilidade_ajustada:
                        neighbor.condition = "On Fire"  # Se a probabilidade for superada, o vizinho começa a pegar fogo
            # Depois de espalhar o fogo, a árvore que pegou fogo passa a estar "queimada".
            self.condition = "Burned Out"  # A árvore já está queimada e não pode mais espalhar fogo.
