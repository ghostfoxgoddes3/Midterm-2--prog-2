import mesa
from model import ForestFire


# Definição de cores para os diferentes estados e agentes
COLORS = {
    "Fine": "#9bf587",  # Árvores saudáveis
    "On Fire": "#FF6666",  # Árvores em chamas
    "Burned Out": "#d4d6d5",  # Árvores queimadas
    "Fire Off": "#6495ED",  # Árvores apagadas por bombeiros
    "terrestre": "#d4a117",  # Bombeiro terrestre
    "aereo": "#1E90FF",  # Bombeiro aéreo
}

def forest_fire_portrayal(agent):
    """
    Função de visualização para exibir os agentes.
    """
    if agent is None:
        return None

    portrayal = {}

    # Representação para bombeiros terrestres e aéreos
    if isinstance(agent, Bombeiro):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Color": COLORS[agent.tipo],  # Cor depende do tipo do bombeiro
            "Layer": 1,
            "w": 1,
            "h": 1,
        }

    # Representação para as árvores
    elif isinstance(agent, TreeCell):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Color": COLORS[agent.condition],  # Cor baseada no estado da árvore
            "Layer": 0,
            "w": 1,
            "h": 1,
        }

    # Adicionando a posição do agente no grid
    if hasattr(agent, "pos"):
        portrayal["x"], portrayal["y"] = agent.pos

    return portrayal

# Canvas para visualização do grid
canvas_element = mesa.visualization.CanvasGrid(
    forest_fire_portrayal, 100, 100, 500, 500
)

# Gráfico de barras para os estados das árvores
tree_chart = mesa.visualization.ChartModule(
    [
        {"Label": "Fine", "Color": COLORS["Fine"]},
        {"Label": "On Fire", "Color": COLORS["On Fire"]},
        {"Label": "Burned Out", "Color": COLORS["Burned Out"]},
        {"Label": "Fire Off", "Color": COLORS["Fire Off"]},
    ]
)

# Gráfico de pizza para a distribuição de estados
pie_chart = mesa.visualization.PieChartModule(
    [
        {"Label": "Fine", "Color": COLORS["Fine"]},
        {"Label": "On Fire", "Color": COLORS["On Fire"]},
        {"Label": "Burned Out", "Color": COLORS["Burned Out"]},
        {"Label": "Fire Off", "Color": COLORS["Fire Off"]},
    ]
)

# Parâmetros do modelo ajustáveis pela interface
model_params = {
    "width": 100,
    "height": 100,
    "density": mesa.visualization.Slider(
        "Tree density", 0.65, 0.01, 1.0, 0.01
    ),
    "prob_de_sobrevivencia": mesa.visualization.Slider(
        "Probability of survival", 0.5, 0.0, 1.0, 0.01
    ),
    "num_pessoas": mesa.visualization.Slider(
        "Number of people", 10, 0, 50, 1
    ),
    "n_bombeiros_terrestres": mesa.visualization.Slider(
        "Terrestrial firefighters", 5, 0, 20, 1
    ),
    "n_bombeiros_aereos": mesa.visualization.Slider(
        "Aerial firefighters", 2, 0, 10, 1
    ),
}

# Inicialização do servidor
server = mesa.visualization.ModularServer(
    ForestFire,
    [canvas_element, tree_chart, pie_chart],
    "Forest Fire Model",
    model_params,
)

server.port = 8521  # Porta padrão para execução do servidor
server.launch()
