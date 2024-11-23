import mesa
from agente3 import TreeCell, CityCell, GrassCell  # Importando as classes TreeCell, CityCell e GrassCell
from model3 import ForestFire  # Importando o modelo de incêndio florestal 

# Definindo as cores para as condições das células
COLORS = {
    "Fine": "#00AA00",        # Verde para árvores/mato saudáveis
    "On Fire": "#880000",     # Vermelho para árvores/mato em chamas
    "Burned Out": "#000000",  # Preto para árvores/mato queimados
    "City": "#0000FF",        # Azul para as cidades
    "Evacuated": "#FFFF00",   # Amarelo para cidades em evacuação
    "Grass Fine": "#7CFC00",  # Verde claro para células de grama saudáveis
    "Grass On Fire": "#FF4500",  # Laranja para células de grama em chamas
    "Grass Burned Out": "#4B4B4B",  # Cinza para células de grama queimadas
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

    # Ajuste para o tamanho da célula dependendo da condição
    if isinstance(cell, CityCell):  # Verificando se é uma cidade
        portrayal["w"] = 5
        portrayal["h"] = 5
        portrayal["Color"] = COLORS[cell.condition] 
    elif isinstance(cell, GrassCell):  # Verificando se é uma célula de grama
        portrayal["w"] = 1
        portrayal["h"] = 1
        if cell.condition == "Fine":
            portrayal["Color"] = COLORS["Grass Fine"]
        elif cell.condition == "On Fire":
            portrayal["Color"] = COLORS["Grass On Fire"]
        elif cell.condition == "Burned Out":
            portrayal["Color"] = COLORS["Grass Burned Out"]
    else:  # Para as árvores
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Color"] = COLORS[cell.condition]

    return portrayal

# Gráfico de barras para mostrar as quantidades de árvores/mato em cada estado
tree_chart = mesa.visualization.ChartModule(
    [
        {"Label": "Fine", "Color": COLORS["Fine"]},
        {"Label": "On Fire", "Color": COLORS["On Fire"]},
        {"Label": "Burned Out", "Color": COLORS["Burned Out"]},
    ]
)

# Gráfico de pizza para a distribuição das árvores e mato
pie_chart = mesa.visualization.PieChartModule(
    [
        {"Label": "Fine", "Color": COLORS["Fine"]},
        {"Label": "On Fire", "Color": COLORS["On Fire"]},
        {"Label": "Burned Out", "Color": COLORS["Burned Out"]},
    ]
)

# Parâmetros do modelo: dimensões da grade, densidade das árvores e probabilidade das cidades
model_params = {
    "height": 100,
    "width": 100,
    "density": mesa.visualization.Slider("Tree density", 0.65, 0.01, 1.0, 0.01),
    "city_probability": mesa.visualization.Slider("City Probability", 0.01, 0.0001, 0.05, 0.0001),
    "grass_probability": mesa.visualization.Slider("Grass Probability", 0.5, 0.01, 1.0, 0.01),
    "prob_de_sobrevivencia": mesa.visualization.Slider("Survival Probability", 0.5, 0.01, 1.0, 0.01),
    "vento": mesa.visualization.Choice("Wind Direction", value="Sem direção", choices=["Norte", "Sul", "Leste", "Oeste", "Sem direção"]),
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
