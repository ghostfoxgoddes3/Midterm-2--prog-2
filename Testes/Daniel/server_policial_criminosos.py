import mesa
from agent import TreeCell, CityCell, GrassCell, GroundFirefighter, AerialFirefighter, Police, Bomber, Logger  # Importando as classes TreeCell, CityCell, GrassCell e Bombeiros
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
    "GroundFirefighter": "#f70202",  # Rosa para o bombeiro
    "Police": "#0000FF",  # Azul para o policial
    "Bomber": "#FF0000",  # Laranja para o Bombardeiro
    "Toasted": "#000000", # Preto para a árvore bombardeada
    "Logger": "#8B4513",  # Marrom para o Logger
    "Blank": "#FFFFFF"    # Branco para a árvore cortada
}

def forest_fire_portrayal(cell):
    """
    Define como cada célula deve ser representada visualmente.
    """
    if cell is None:
        return None

    portrayal = {"Shape": None, "Filled": "true", "Layer": 0, "Color": "#000000"}

    if isinstance(cell, AerialFirefighter):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 5
        portrayal["Layer"] = 2  # Bombeiro em uma camada superior
        portrayal["Color"] = COLORS["GroundFirefighter"]

    elif isinstance(cell, GroundFirefighter):
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
        
        # Policial
    if isinstance(cell, Police):
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Color": COLORS["Police"],
            "Layer": 3,
            "r": 2,  # Raio do círculo
        }

    # Bombardeiro
    elif isinstance(cell, Bomber):
        # Verifica se o Bombardeiro foi capturado e altera a cor para Roxo
        if cell.captured:
            portrayal = {
                "Shape": "circle",
                "Filled": "true",
                "Color": "#A020F0",  # Roxo
                "Layer": 3,
                "r": 2,
            }
        else:
            portrayal = {
                "Shape": "circle",
                "Filled": "true",
                "Color": COLORS["Bomber"],
                "Layer": 3,
                "r": 2,
            }
     # Logger (Madeireiro)
    elif isinstance(cell, Logger):
        # Verifica se o Madeireiro foi capturado e altera a cor para Roxo
        if cell.captured:
            portrayal = {
                "Shape": "circle",
                "Filled": "true",
                "Color": "#A020F0", 
                "Layer": 3,
                "r": 2,
            }
        else:
            portrayal = {
                "Shape": "circle",
                "Filled": "true",
                "Color": COLORS["Logger"],
                "Layer": 3,
                "r": 2,
            }

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
        {"Label": "Fire Off", "Color": COLORS["Fire Off"]},
    ]
)

# Gráfico de pizza para distribuição de árvores
pie_chart = mesa.visualization.PieChartModule(
    [
        {"Label": "Fine", "Color": COLORS["Fine"]},
        {"Label": "On Fire", "Color": COLORS["On Fire"]},
        {"Label": "Burned Out", "Color": COLORS["Burned Out"]},
        {"Label": "Fire Off", "Color": COLORS["Fire Off"]},
    ]
)

# Parâmetros do modelo
model_params = {
    "height": 100,
    "width": 100,
    "density": mesa.visualization.Slider("Densidade de Árvore", 0.65, 0.01, 1.0, 0.01),
    "city_probability": mesa.visualization.Slider("Densidade de Cidades", 0.01, 0.0001, 0.05, 0.0001),
    "grass_probability": mesa.visualization.Slider("Sobrevivência da grama", 0.5, 0.01, 1.0, 0.01),
    "prob_de_sobrevivencia": mesa.visualization.Slider("Resistência da árvore ao fogo", 0.5, 0.01, 1.0, 0.01),
    "vento": mesa.visualization.Choice("Direção do vento", value="Sem direção", choices=["Norte", "Sul", "Leste", "Oeste", "Sem direção"]),
    "num_pessoas": mesa.visualization.Slider("Número de bombeiros terrestres", 10, 0, 50, 1),
    "num_helicoptero": mesa.visualization.Slider("Número de helicopteros", 5, 0, 10, 1),
    "num_policiais": mesa.visualization.Slider("Número de Policiais", 5, 0, 20, 1),
    "num_bombers": mesa.visualization.Slider("Número de Bombardeiros", 3, 0, 20, 1),
    "num_loggers": mesa.visualization.Slider("Número de Madeireiros", 2, 0, 20, 1),
}

# Canvas para visualização
canvas_element = mesa.visualization.CanvasGrid(
    forest_fire_portrayal, 100, 100, 500, 500
)

# Inicializando o servidor
server = mesa.visualization.ModularServer(
    ForestFire, [canvas_element, tree_chart, pie_chart], "Forest Fire com Cidades e Pessoas", model_params
)

# Porta do servidor
server.port = 8521
server.launch()
