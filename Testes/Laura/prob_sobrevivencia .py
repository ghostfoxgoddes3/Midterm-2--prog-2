
def calcular_probabilidade_sobrevivencia(arvore, modelo, fator_resistencia=0.5):
    """
    Calcula a probabilidade de uma árvore sobreviver ao incêndio com base nos vizinhos em chamas 
    e em um fator de resistência individual.

    Args:
        arvore: A árvore (agente) que estamos analisando.
        modelo: O modelo de simulação do incêndio (ForestFire).
        fator_resistencia: Valor entre 0 e 1 que representa o quanto a árvore é resistente ao fogo 
                           (1 significa resistência máxima).

    Returns:
        probabilidade_sobrevivencia: Valor entre 0 e 1 indicando a chance de a árvore sobreviver.
    """
    # Se a árvore já está em chamas ou queimada, não pode sobreviver
    if arvore.condition != "Fine":
        return 0.0

    # Obtém os vizinhos da árvore na grade
    vizinhos = modelo.grid.get_neighbors(arvore.pos, moore=True, include_center=False)

    # Conta quantas árvores vizinhas estão "On Fire"
    vizinhos_em_chamas = sum(
        1 for vizinho in vizinhos 
        if hasattr(vizinho, 'condition') and vizinho.condition == "On Fire"
    )

    # Calcula a probabilidade de sobrevivência
    chance_base = max(0, 1 - (vizinhos_em_chamas / 8))  # Considera até 8 vizinhos possíveis
    chance_sobrevivencia = chance_base * fator_resistencia

    return chance_sobrevivencia

# Exemplo de uso:
# Supondo que 'modelo' seja o modelo ForestFire e 'arvore' seja uma instância de TreeCell
probabilidade = calcular_probabilidade_sobrevivencia(arvore, modelo)
print(f"A probabilidade de sobrevivência da árvore é de: {probabilidade:.2%}")
