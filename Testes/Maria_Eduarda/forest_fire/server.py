import mesa
from model import ForestFire

# Emojis e cores personalizadas para os diferentes estados das árvores
EMOJIS = {"Fine": "v", "On Fire": "🔥", "Burned Out": "♥"}
COLORS = {"Fine": "#66FF66", "On Fire": "#FF6666", "Burned Out": "#999999"}

def forest_fire_portrayal(tree):
    if tree is None:
        return
    
    # Configuração do portrayal para incluir emojis e cores
    portrayal = {
        "Shape": "rect",  # Forma como retângulo para permitir a cor de fundo
        "Filled": "true",
        "Layer": 0,
        "Color": COLORS[tree.condition],  # Cor de fundo personalizada para o estado
        "text": EMOJIS[tree.condition],  # Emoji para ilustrar o estado
        "text_color": "black",  # Cor do emoji para contraste
        "w": 1,  # Largura da célula
        "h": 1,  # Altura da célula
    }
    (x, y) = tree.pos
    portrayal["x"] = x
    portrayal["y"] = y
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

# Parâmetros do modelo (dimensões do grid e densidade das árvores)
model_params = {
    "height": 100,
    "width": 100,
    "density": mesa.visualization.Slider("Tree density", 0.65, 0.01, 1.0, 0.01),
}

# Inicializando o servidor
server = mesa.visualization.ModularServer(
    ForestFire, [canvas_element, tree_chart, pie_chart], "Forest Fire", model_params
)

server.port = 8521  # Porta do servidor
server.launch()
