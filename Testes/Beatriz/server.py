import mesa
from model import ForestFire

COLORS = {"Fine": "#46951e", "On Fire": "#FF6666", "Burned Out": "#4d305f"}


def forest_fire_portrayal(tree):
    if tree is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    (x, y) = tree.pos
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = COLORS[tree.condition]
    return portrayal

# Definindo o Canvas para a visualização do modelo
canvas_element = mesa.visualization.CanvasGrid(
    forest_fire_portrayal, 100, 100, 500, 500
)

# Gráfico de barras para as árvores
tree_chart = mesa.visualization.ChartModule(
    [{"Label": label, "Color": color} for label, color in COLORS.items()]
)

# Gráfico de pizza para a distribuição das árvores
pie_chart = mesa.visualization.PieChartModule(
    [{"Label": label, "Color": color} for label, color in COLORS.items()]
)

# Parâmetros do modelo (dimensões do grid, densidade das árvores, probabilidade de sobrevivência e direção do vento)
model_params = {
    "height": 100,
    "width": 100,
    "density": mesa.visualization.Slider("Tree density", 0.65, 0.01, 1.0, 0.01),
    "prob_de_sobrevivencia": mesa.visualization.Slider("Probability of survival", 0.5, 0.0, 1.0, 0.01),
    "vento": mesa.visualization.Choice("Wind Direction", value="Sem direção", choices=["Norte", "Sul", "Leste", "Oeste", "Sem direção"])
}

# Inicializando o servidor
server = mesa.visualization.ModularServer(
    ForestFire, [canvas_element, tree_chart, pie_chart], "Forest Fire", model_params
)

server.port = 8521  # Porta do servidor
server.launch()
