import mesa
from model import ForestFire, TreeCell, Police, Bomber, Logger

# Cores para os diferentes estados e agentes
COLORS = {
    "Fine": "#9bf587",  # Cor para árvores saudáveis
    "On Fire": "#FF6666",  # Cor para árvores pegando fogo
    "Burned Out": "#d4d6d5",  # Cor para árvores queimadas
    "Fire Off": "#6495ED",  # Cor para árvore apagada pelo bombeiro
    "Police": "#0000FF",  # Cor do policial
    "Bomber": "#FF0000",  # Cor do Bombardeiro
    "Toasted": "#000000", #Cor da Árvore bombardeada
    "Logger": "#8B4513",  # Cor do Logger (Madeireiro)
    "Blank": "#FFFFFF"
}

def forest_fire_portrayal(agent):
    """
    Função para exibir visualmente as árvores policiais e Bombardeiros.
    """
    if agent is None:
        return None

    portrayal = {}  # Inicializando o dicionário de visualização


    # Policial
    if isinstance(agent, Police):
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Color": COLORS["Police"],
            "Layer": 3,
            "r": 2,  # Raio do círculo
        }

    # Bombardeiro
    elif isinstance(agent, Bomber):
        # Verifica se o Bombardeiro foi capturado e altera a cor para Roxo
        if agent.captured:
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
    elif isinstance(agent, Logger):
        # Verifica se o Madeireiro foi capturado e altera a cor para Roxo
        if agent.captured:
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
    "num_policiais": mesa.visualization.Slider("Number of police officers", 5, 0, 20, 1),
    "num_bombers": mesa.visualization.Slider("Number of Bombers", 3, 0, 20, 1),
    "num_loggers": mesa.visualization.Slider("Number of loggers", 2, 0, 20, 1),
}

# Inicializando o servidor
server = mesa.visualization.ModularServer(
    ForestFire, [canvas_element, tree_chart, pie_chart], "Forest Fire Simulation", model_params
)

server.port = 8521  # Porta do servidor
server.launch()
