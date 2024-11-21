import mesa
from model import ForestFire, TreeCell, GroundFirefighter, Police, Incendiary

# Cores para os diferentes estados e agentes
COLORS = {
    "Fine": "#9bf587",  # Cor para árvores saudáveis
    "On Fire": "#FF6666",  # Cor para árvores pegando fogo
    "Burned Out": "#d4d6d5",  # Cor para árvores queimadas
    "Fire Off": "#6495ED",  # Cor para árvore apagada pelo bombeiro
    "GroundFirefighter": "#d4a117",  # Cor do bombeiro
    "Police": "#0000FF",  # Cor do policial
    "Incendiary": "#FF4500",  # Cor do incendiário
}

def forest_fire_portrayal(agent):
    """
    Função para exibir visualmente as árvores, bombeiros, policiais e incendiários.
    """
    if agent is None:
        return None

    portrayal = {}  # Inicializando o dicionário de visualização

    # Bombeiro terrestre
    if isinstance(agent, GroundFirefighter):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Color": COLORS["GroundFirefighter"],
            "Layer": 2,
            "w": 1,
            "h": 1,
        }

    # Policial
    elif isinstance(agent, Police):
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Color": COLORS["Police"],
            "Layer": 3,
            "r": 0.5,  # Raio do círculo
        }

    # Incendiário
    elif isinstance(agent, Incendiary):
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Color": COLORS["Incendiary"],
            "Layer": 3,
            "r": 0.5,
        }

    # Árvore
    elif isinstance(agent, TreeCell):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Color": COLORS[agent.condition],
            "Layer": 0,
            "w": 1,
            "h": 1,
        }

    # Coordenadas no grid
    x, y = agent.pos
    portrayal["x"] = x
    portrayal["y"] = y

    return portrayal

# Canvas para exibir o grid
canvas_element = mesa.visualization.CanvasGrid(
    forest_fire_portrayal, 100, 100, 500, 500
)

# Gráficos de barras
tree_chart = mesa.visualization.ChartModule(
    [
        {"Label": "Fine", "Color": COLORS["Fine"]},
        {"Label": "On Fire", "Color": COLORS["On Fire"]},
        {"Label": "Burned Out", "Color": COLORS["Burned Out"]},
        {"Label": "Fire Off", "Color": COLORS["Fire Off"]},
    ]
)

# Gráficos de pizza
pie_chart = mesa.visualization.PieChartModule(
    [
        {"Label": "Fine", "Color": COLORS["Fine"]},
        {"Label": "On Fire", "Color": COLORS["On Fire"]},
        {"Label": "Burned Out", "Color": COLORS["Burned Out"]},
        {"Label": "Fire Off", "Color": COLORS["Fire Off"]},
    ]
)

# Parâmetros do modelo configuráveis pelo usuário
model_params = {
    "height": 100,
    "width": 100,
    "density": mesa.visualization.Slider("Tree density", 0.65, 0.01, 1.0, 0.01),
    "prob_de_sobrevivencia": mesa.visualization.Slider("Probability of survival", 0.5, 0.0, 1.0, 0.01),
    "num_pessoas": mesa.visualization.Slider("Number of fire fighters", 10, 0, 50, 1),
    "num_policiais": mesa.visualization.Slider("Number of police officers", 5, 0, 20, 1),
    "num_incendiarios": mesa.visualization.Slider("Number of incendiaries", 3, 0, 20, 1),
}

# Inicializando o servidor
server = mesa.visualization.ModularServer(
    ForestFire, [canvas_element, tree_chart, pie_chart], "Forest Fire Simulation", model_params
)

server.port = 8521  # Porta do servidor
server.launch()
