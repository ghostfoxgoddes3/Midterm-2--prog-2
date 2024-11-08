import mesa
from model import ForestFire  # Certifique-se que o arquivo model.py tem a classe ForestFire

# Define as cores para os estados das árvores
COLORS = {"Fine": "#00AA00", "On Fire": "#880000", "Burned Out": "#000000"}

def forest_fire_portrayal(tree):
    """Definição da visualização padrão para cada árvore."""
    if tree is None:
        return

    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    (x, y) = tree.pos
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = COLORS[tree.condition]

    # Seta de vento no centro do grid
    center_x, center_y = tree.model.grid.width // 2, tree.model.grid.height // 2
    if (x, y) == (center_x, center_y):
        portrayal = {
            "Shape": "arrowHead",
            "scale": 1.5,
            "Color": "blue",
            "Filled": "true",
            "Layer": 1,
            "x": x,
            "y": y,
        }
        # Direção da seta com base no vento
        directions = {"Norte": 0, "Sul": 180, "Leste": 90, "Oeste": 270}
        if tree.model.wind_direction in directions:
            portrayal["heading_x"] = 0.5 if tree.model.wind_direction == "Leste" else -0.5
            portrayal["heading_y"] = 0.5 if tree.model.wind_direction == "Norte" else -0.5
        else:
            portrayal["Color"] = "gray"  # Sem vento

    return portrayal

# Função para visualização alternativa em estilo de mapa de calor
def heatmap_portrayal(tree):
    if tree is None:
        return
    
    # Cores para visualização em mapa de calor
    colors_heatmap = {"Fine": "#D3FFD3", "On Fire": "#FF8C00", "Burned Out": "#8B0000"}
    portrayal = {
        "Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0,
        "x": tree.pos[0], "y": tree.pos[1], "Color": colors_heatmap[tree.condition]
    }
    return portrayal

# Interface padrão de visualização
canvas_element = mesa.visualization.CanvasGrid(forest_fire_portrayal, 100, 100, 500, 500)

# Interface de visualização alternativa
heatmap_canvas = mesa.visualization.CanvasGrid(heatmap_portrayal, 100, 100, 500, 500)

# Gráficos de barra e pizza para o estado do fogo
tree_chart = mesa.visualization.ChartModule(
    [{"Label": label, "Color": color} for label, color in COLORS.items()]
)
pie_chart = mesa.visualization.PieChartModule(
    [{"Label": label, "Color": color} for label, color in COLORS.items()]
)

# Parâmetros do modelo e inicialização do servidor
model_params = {
    "height": 100,
    "width": 100,
    "density": mesa.visualization.Slider("Tree density", 0.65, 0.01, 1.0, 0.01),
}

# Função para iniciar o fogo em uma árvore ao clicar nela
def on_click_tree(agent, pos):
    if agent.condition == "Fine":
        agent.condition = "On Fire"

# Configuração do canvas para o evento de clique
canvas_element.set_on_click(on_click_tree)

# Inicialização do servidor com ambas as visualizações
server = mesa.visualization.ModularServer(
    ForestFire, 
    [canvas_element, tree_chart, pie_chart, heatmap_canvas],  # Adicionando as visualizações
    "Forest Fire with Heatmap",
    model_params
)

server.port = 8521
server.launch()
