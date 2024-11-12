import mesa
from model import ForestFire
from agent import TreeCell
from bombeiro import GroundFirefighter

# Definindo as cores para os estados das árvores
COLORS = {
    "Fine": "#00AA00",  # Árvore saudável
    "On Fire": "#880000",  # Árvore pegando fogo
    "Burned Out": "#000000",  # Árvore queimada
    "Fire Off": "#AAAAAA"  # Árvore apagada
}

def forest_fire_portrayal(agent):
    """Define como as árvores e bombeiros serão visualizados no grid"""
    if agent is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    portrayal["x"] = agent.pos[0]
    portrayal["y"] = agent.pos[1]
    
    if isinstance(agent, TreeCell):
        portrayal["Color"] = COLORS.get(agent.condition, "#AAAAAA")  # Cor para os diferentes estados das árvores
    else:
        portrayal["Color"] = "#0000FF"  # Cor para o bombeiro (azul)
    
    return portrayal

# Grid e gráficos
canvas_element = mesa.visualization.CanvasGrid(forest_fire_portrayal, 100, 100, 500, 500)
tree_chart = mesa.visualization.ChartModule(
    [{"Label": label, "Color": color} for label, color in COLORS.items() if label != "Fire Off"]
)
pie_chart = mesa.visualization.PieChartModule(
    [{"Label": label, "Color": color} for label, color in COLORS.items() if label != "Fire Off"]
)

# Parâmetros do modelo
model_params = {
    "width": 100,
    "height": 100,
    "density": mesa.visualization.Slider("Tree density", 0.65, 0.01, 1.0, 0.01)
}

server = mesa.visualization.ModularServer(
    ForestFire, [canvas_element, tree_chart, pie_chart], "Forest Fire", model_params
)

server.port = 8521
server.launch()
