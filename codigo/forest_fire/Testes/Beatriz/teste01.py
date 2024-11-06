import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Configurações
tamanho = 50  # Tamanho da grade (50x50)
prob_arvore = 0.6  # Probabilidade de uma célula ser uma árvore
prob_fogo = 0.01  # Probabilidade de ignição espontânea
prob_propagacao = 0.3  # Probabilidade de propagação do fogo para árvores vizinhas

# Inicializa a floresta
floresta = np.random.choice([0, 1], (tamanho, tamanho), p=[1 - prob_arvore, prob_arvore])

# Função para atualização do estado da floresta
def atualiza_floresta(floresta):
    nova_floresta = floresta.copy()
    for i in range(tamanho):
        for j in range(tamanho):
            if floresta[i, j] == 1:  # Se a célula é uma árvore
                if np.random.rand() < prob_fogo:  # Ignição espontânea
                    nova_floresta[i, j] = 2
                # Verifica se há fogo nas células vizinhas
                elif any(floresta[max(0, i - 1):min(tamanho, i + 2), max(0, j - 1):min(tamanho, j + 2)].flatten() == 2):
                    if np.random.rand() < prob_propagacao:
                        nova_floresta[i, j] = 2
            elif floresta[i, j] == 2:  # Se a célula está em chamas
                nova_floresta[i, j] = 0  # Apaga a árvore (transforma em vazio)
    return nova_floresta

# Configura a coloração
cmap = mcolors.ListedColormap(['white', 'green', 'red'])
bounds = [0, 0.5, 1.5, 2.5]
norm = mcolors.BoundaryNorm(bounds, cmap.N)

# Simulação
num_iteracoes = 20
for t in range(num_iteracoes):
    plt.imshow(floresta, cmap=cmap, norm=norm)
    plt.title(f"Iteração {t}")
    plt.axis('off')
    plt.pause(0.5)
    floresta = atualiza_floresta(floresta)

plt.show()
