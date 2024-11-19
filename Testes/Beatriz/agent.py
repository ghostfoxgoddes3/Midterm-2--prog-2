import mesa

class TreeCell(mesa.Agent):
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
        self.condition = "Fine"
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
          # Define diferentes incrementos para direções do vento
        if self.model.vento == "Norte":
            incremento_vento = 0.7  # Aumenta o impacto do vento Norte
        elif self.model.vento == "Sul":
            incremento_vento = 0.7 # Aumenta o impacto do vento Sul
        else:
            incremento_vento = 0.5  # Para Leste/Oeste, o impacto é um pouco menor
        

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
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if neighbor.condition == "Fine":
                    # Ajustar a probabilidade com base no vento
                    probabilidade_ajustada = neighbor.ajusta_probabilidade_por_vento(self.pos)
                    
                    # Verificar probabilidade ajustada para pegar fogo
                    if self.random.random() > probabilidade_ajustada:
                        neighbor.condition = "On Fire"
            # Alterar a condição da árvore para "Burned Out"
            self.condition = "Burned Out"
