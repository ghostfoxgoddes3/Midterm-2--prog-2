import mesa
from model import ForestFire

COLORS = {"Fine": "#00AA00", "On Fire": "#880000", "Burned Out": "#000000"}

def forest_fire_portrayal(tree):
    if tree is None:
        return

    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    (x, y) = tree.pos
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = COLORS[tree.condition]

    # Verifica se é o centro do grid e insere a seta de vento
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

        # Define a direção da seta de acordo com o vento
        directions = {"Norte": 0, "Sul": 180, "Leste": 90, "Oeste": 270}
        if tree.model.wind_direction in directions:
            portrayal["heading_x"] = 0.5 if tree.model.wind_direction == "Leste" else -0.5
            portrayal["heading_y"] = 0.5 if tree.model.wind_direction == "Norte" else -0.5
        else:
            portrayal["Color"] = "gray"  # Sem vento

    return portrayal

# Gráfico de visualização do estado das árvores
canvas_element = mesa.visualization.CanvasGrid(forest_fire_portrayal, 100, 100, 500, 500)

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

server = mesa.visualization.ModularServer(
    ForestFire, [canvas_element, tree_chart, pie_chart], "Forest Fire", model_params
)

server.port = 8521
server.launch()
