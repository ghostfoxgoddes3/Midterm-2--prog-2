def encontrar_ponto_incendio_mais_intenso(modelo, tamanho_janela=3):
    """
    Encontra o ponto de incêndio mais intenso na floresta.
    A função verifica janelas de tamanho (tamanho_janela x tamanho_janela) 
    e conta o número de células em estado "On Fire".

    Args:
        modelo: Instância do modelo ForestFire.
        tamanho_janela: Tamanho da janela (subgrade) para análise.
    
    Returns:
        (intensidade, (x, y)): A intensidade (quantidade de árvores "On Fire") 
        e as coordenadas do canto superior esquerdo da janela.
    """
    intensidade_maxima = 0
    melhor_localizacao = None

    largura_grid = modelo.grid.width
    altura_grid = modelo.grid.height

    # Percorre possíveis locais de início da janela na grade
    for x in range(largura_grid - tamanho_janela + 1):
        for y in range(altura_grid - tamanho_janela + 1):
            # Conta o número de células "On Fire" na janela atual
            contador_fogo = 0
            for desloc_x in range(tamanho_janela):
                for desloc_y in range(tamanho_janela):
                    # Obtém os agentes presentes na célula específica
                    conteudo_celula = modelo.grid.get_cell_list_contents([(x + desloc_x, y + desloc_y)])
                    for agente in conteudo_celula:
                        if hasattr(agente, 'condition') and agente.condition == "On Fire":
                            contador_fogo += 1
            # Verifica se esta janela tem a maior intensidade encontrada
            if contador_fogo > intensidade_maxima:
                intensidade_maxima = contador_fogo
                melhor_localizacao = (x, y)

    return intensidade_maxima, melhor_localizacao

