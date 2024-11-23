import mesa
from agent import TreeCell, CityCell, GrassCell, GroundFirefighter  # Importando as classes TreeCell, CityCell, GrassCell e Bombeiros
from model import ForestFire  # Importando o modelo de incêndio florestal 

# Definindo as cores para as condições das células
COLORS = {
    "Fine": "#7eed24",        # Verde para árvores saudáveis
    "On Fire": "#f7981b",     # Vermelho para árvores em chamas
    "Burned Out": "#c9c7c9",  # Preto para árvores queimadas
    "City": "#e877fc",        # Azul para as cidades
    "Evacuated": "#FFFF00",   # Amarelo para cidades em evacuação
    "Grass Fine": "#c2fa93",  # Verde claro para gramas saudáveis
    "Grass On Fire": "#f5a031",  # Laranja para gramas em chamas
    "Grass Burned Out": "#a8a8a8",  # Cinza para gramas queimadas
    "Fire Off": "#0000FF",    # Azul claro para árvore apagada pelo bombeiro
    "GroundFirefighter": "#f70202"  # Rosa para o bombeiro
}

def forest_fire_portrayal(cell):
    """
    Define como cada célula deve ser representada visualmente.
    """
    if cell is None:
        return None

    portrayal = {"Shape": None, "Filled": "true", "Layer": 0, "Color": "#000000"}

    if isinstance(cell, GroundFirefighter):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.8
        portrayal["Layer"] = 1  # Bombeiro em uma camada superior
        portrayal["Color"] = COLORS["GroundFirefighter"]

    elif isinstance(cell, TreeCell):
        portrayal["Shape"] = "rect"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Color"] = COLORS[cell.condition]
        portrayal["Layer"] = 0  # Árvore em camada inferior

    elif isinstance(cell, CityCell):
        portrayal["Shape"] = "rect"
        portrayal["w"] = 5
        portrayal["h"] = 5
        portrayal["Color"] = COLORS[cell.condition]
        portrayal["Layer"] = 0

    elif isinstance(cell, GrassCell):
        portrayal["Shape"] = "rect"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Layer"] = 0
        if cell.condition == "Fine":
            portrayal["Color"] = COLORS["Grass Fine"]
        elif cell.condition == "On Fire":
            portrayal["Color"] = COLORS["Grass On Fire"]
        elif cell.condition == "Burned Out":
            portrayal["Color"] = COLORS["Grass Burned Out"]

    # Coordenadas da célula
    (x, y) = cell.pos
    portrayal["x"] = x
    portrayal["y"] = y

    return portrayal


# Gráficos de estatísticas
tree_chart = mesa.visualization.ChartModule(
    [
        {"Label": "Fine", "Color": COLORS["Fine"]},
        {"Label": "On Fire", "Color": COLORS["On Fire"]},
        {"Label": "Burned Out", "Color": COLORS["Burned Out"]},
    ]
)

# Gráfico de pizza para distribuição de árvores
pie_chart = mesa.visualization.PieChartModule(
    [
        {"Label": "Fine", "Color": COLORS["Fine"]},
        {"Label": "On Fire", "Color": COLORS["On Fire"]},
        {"Label": "Burned Out", "Color": COLORS["Burned Out"]},
    ]
)

# Parâmetros do modelo
model_params = {
    "height": 100,
    "width": 100,
    "density": mesa.visualization.Slider("Tree density", 0.65, 0.01, 1.0, 0.01),
    "city_probability": mesa.visualization.Slider("City Probability", 0.01, 0.0001, 0.05, 0.0001),
    "grass_probability": mesa.visualization.Slider("Grass Probability", 0.5, 0.01, 1.0, 0.01),
    "prob_de_sobrevivencia": mesa.visualization.Slider("Survival Probability", 0.5, 0.01, 1.0, 0.01),
    "vento": mesa.visualization.Choice("Wind Direction", value="Sem direção", choices=["Norte", "Sul", "Leste", "Oeste", "Sem direção"]),
    "num_pessoas": mesa.visualization.Slider("Number of fire fighters", 10, 0, 50, 1),
}

# Canvas para visualização
canvas_element = mesa.visualization.CanvasGrid(
    forest_fire_portrayal, 100, 100, 500, 500
)

# Inicializando o servidor
server = mesa.visualization.ModularServer(
    ForestFire, [canvas_element, tree_chart, pie_chart], "Forest Fire with Cities and Evacuation", model_params
)

# Porta do servidor
server.port = 8521
server.launch()
