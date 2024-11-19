import mesa
from agent import TreeCell, CityCell  # Importando as classes TreeCell e CityCell
from model import ForestFire  # Importando o modelo de incêndio florestal

# Definindo as cores para as condições das células
COLORS = {
    "Fine": "#00AA00",        # Verde para árvores saudáveis
    "On Fire": "#880000",     # Vermelho para árvores em chamas
    "Burned Out": "#000000",  # Preto para árvores queimadas
    "City": "#0000FF",        # Azul para as cidades
    "Evacuated": "#FFFF00"    # Amarelo para cidades em evacuação
}

def forest_fire_portrayal(cell):
    """
    Define como cada célula deve ser representada visualmente.
    """
    if cell is None:
        return

    portrayal = {"Shape": "rect", "Filled": "true", "Layer": 0}
    (x, y) = cell.pos
    portrayal["x"] = x
    portrayal["y"] = y

    # Ajuste para o tamanho da célula dependendo da condição (cidade é 5x5)
    if isinstance(cell, CityCell):  # Verificando se é uma cidade
        portrayal["w"] = 5
        portrayal["h"] = 5
    else:  # Para as árvores
        portrayal["w"] = 1
        portrayal["h"] = 1

    portrayal["Color"] = COLORS[cell.condition]  # A cor da célula depende da sua condição
    return portrayal

# Gráfico de barras para mostrar as quantidades de árvores em cada estado
tree_chart = mesa.visualization.ChartModule(
    [{"Label": label, "Color": color} for label, color in COLORS.items() if label != "City" and label != "Evacuated"]
)

# Gráfico de pizza para a distribuição das árvores
pie_chart = mesa.visualization.PieChartModule(
    [{"Label": label, "Color": color} for label, color in COLORS.items() if label != "City" and label != "Evacuated"]
)

# Parâmetros do modelo: dimensões da grade, densidade das árvores e probabilidade das cidades
model_params = {
    "height": 100,
    "width": 100,
    "density": mesa.visualization.Slider("Tree density", 0.65, 0.01, 1.0, 0.01),
    "city_probability": mesa.visualization.Slider("City Probability", 0.01, 0.0001, 0.05, 0.0001),
    "prob_de_sobrevivencia": mesa.visualization.Slider("Survival Probability", 0.5, 0.01, 1.0, 0.01),
    "vento": mesa.visualization.Choice("Wind Direction", value="Sem direção", choices=["Norte", "Sul", "Leste", "Oeste", "Sem direção"])
}

# Definindo o Canvas para a visualização do modelo
canvas_element = mesa.visualization.CanvasGrid(
    forest_fire_portrayal, 100, 100, 500, 500
)

# Inicializando o servidor com o modelo, a visualização e os parâmetros
server = mesa.visualization.ModularServer(
    ForestFire, [canvas_element, tree_chart, pie_chart], "Forest Fire with Cities and Evacuation", model_params
)

# Configurando a porta para o servidor
server.port = 8521
server.launch()
