import mesa
from model import ForestFire, Person, TreeCell, GroundFirefighter
#from bombeiro import GroundFirefighter

# Cores para os diferentes estados das árvores e das pessoas
COLORS = {
    "Fine": "#9bf587",  # Cor para árvores saudáveis
    "On Fire": "#FF6666",  # Cor para árvores pegando fogo
    "Burned Out": "#d4d6d5",  # Cor para árvores queimadas
    "Fire Off": "#6495ED", # Cor para árvore apagada pelo bombeiro
    "GroundFirefighter": "#d4a117" # Cor do bombeiro
    #"Alive": "#FF66CC",  # Cor de rosa para pessoas vivas
    #"Dead": "#111212"  # Cor cinza para pessoas mortas
}

def forest_fire_portrayal(agent):
    """
    Função para exibir visualmente as árvores e pessoas.
    """
    if agent is None:
        return None
    
    portrayal = {}  # Inicializando o dicionário de visualização

    if isinstance(agent, GroundFirefighter):
        # Representação para o bombeiro terrestre
        portrayal = {
            "Shape": "rect",  # Forma retangular das células
            "Filled": "true",
            "Color": COLORS["GroundFirefighter"],  # Cor do bombeiro
            "Layer": 1,  # Camada do bombeiro
            "w": 1,  # Largura da célula
            "h": 1  # Altura da célula
        }

            
    # Verificar se o agente é uma árvore ou uma pessoa
    if isinstance(agent, TreeCell):
        # Representação para as árvores
        portrayal = {
            "Shape": "rect",  # Forma retangular das células
            "Filled": "true",
            "Color": COLORS[agent.condition],  # Cor da árvore com base no estado
            "Layer": 0,  # Camada das árvores
            "w": 1,  # Largura da célula
            "h": 1  # Altura da célula
        }

    # Posições no grid
    x, y = agent.pos
    portrayal["x"] = x
    portrayal["y"] = y
    
    return portrayal

# Definindo o Canvas para a visualização do modelo
canvas_element = mesa.visualization.CanvasGrid(
    forest_fire_portrayal, 100, 100, 500, 500
)

# Gráfico de barras para as árvores
tree_chart = mesa.visualization.ChartModule(
    [{"Label": label, "Color": color} for label, color in COLORS.items() if label != "Alive" and label != "Dead"]
)

# Gráfico de pizza para a distribuição das árvores e pessoas
pie_chart = mesa.visualization.PieChartModule(
    [{"Label": label, "Color": color} for label, color in COLORS.items() if label != "Alive" and label != "Dead"]
)

# Parâmetros do modelo (dimensões do grid, densidade das árvores e probabilidade de sobrevivência)
model_params = {
    "height": 100,
    "width": 100,
    "density": mesa.visualization.Slider("Tree density", 0.65, 0.01, 1.0, 0.01),
    "prob_de_sobrevivencia": mesa.visualization.Slider("Probability of survival", 0.5, 0.0, 1.0, 0.01),
    "num_pessoas": mesa.visualization.Slider("Number of fire figthers", 10, 0, 50, 1),  # Ajuste o número de pessoas
}

# Inicializando o servidor
server = mesa.visualization.ModularServer(
    ForestFire, [canvas_element, tree_chart, pie_chart], "Forest Fire", model_params
)

server.port = 8521  # Porta do servidor
server.launch()