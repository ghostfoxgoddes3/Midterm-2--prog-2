import mesa
from model import ForestFire, Person, TreeCell

# Cores para os diferentes estados das árvores e das pessoas
COLORS = {
    "Fine": "#9bf587",  # Cor para árvores saudáveis
    "On Fire": "#FF6666",  # Cor para árvores pegando fogo
    "Burned Out": "#d4d6d5",  # Cor para árvores queimadas
    "Alive": "#FF66CC",  # Cor de rosa para pessoas vivas
    "Dead": "#111212"  # Cor cinza para pessoas mortas
}

def forest_fire_portrayal(agent):
    """
    Função para exibir visualmente as árvores e pessoas.
    """
    if agent is None:
        return None
    
    portrayal = {}  # Inicializando o dicionário de visualização

    if isinstance(agent, Person):
        # Representação para as pessoas
        portrayal["Layer"] = 1  # Camada para as pessoas, acima das árvores
        if agent.condition == "Alive":
            portrayal = {
                "Shape": "circle",  # Forma circular para pessoas vivas
                "Filled": "true",
                "Color": COLORS["Alive"],  # Cor para pessoas vivas
                "Layer": 1,  # Camada das pessoas
                "r": 0.5  # Raio do círculo
            }
        elif agent.condition == "Dead":
            portrayal = {
                "Shape": "rect",  # Forma retangular para pessoas mortas
                "Filled": "true",
                "Color": COLORS["Dead"],  # Cor para pessoas mortas
                "Layer": 1,  # Camada das pessoas
                "w": 1,  # Largura da célula
                "h": 1  # Altura da célula
            }
            
    # Verificar se o agente é uma árvore ou uma pessoa
    if isinstance(agent, TreeCell):
        # Representação para as árvores
        if agent.condition == "Fine":
            text = "v"  # Árvore saudável
        elif agent.condition == "On Fire":
            text = "🔥"  # Árvore pegando fogo
        elif agent.condition == "Burned Out":
            text = "♥"  # Árvore queimada
        
        portrayal["Color"] = COLORS[agent.condition]  # Cor das árvores
        portrayal["text"] = text  # Emoji para as árvores
        portrayal["text_color"] = COLORS[agent.condition]  # Cor do emoji para árvores

    elif isinstance(agent, Person):
        # Representação para as pessoas
        if agent.condition == "Alive":
            text = ""  # Pessoa viva (emoji)
            portrayal["Color"] = COLORS["Alive"]  # Cor de rosa para pessoas vivas
        elif agent.condition == "Dead":
            text = "💀"  # Pessoa morta (emoji)
            portrayal["Color"] = COLORS["Dead"]  # Cor cinza para pessoas mortas

        portrayal["text"] = text  # Emoji para pessoas
        portrayal["text_color"] = COLORS[agent.condition]  # Cor do emoji para pessoas
        portrayal["Layer"] = 1  # Camada para as pessoas, acima das árvores

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
    [{"Label": label, "Color": color} for label, color in COLORS.items()]
)

# Parâmetros do modelo (dimensões do grid, densidade das árvores e probabilidade de sobrevivência)
model_params = {
    "height": 100,
    "width": 100,
    "density": mesa.visualization.Slider("Tree density", 0.65, 0.01, 1.0, 0.01),
    "prob_de_sobrevivencia": mesa.visualization.Slider("Probability of survival", 0.5, 0.0, 1.0, 0.01),
    "num_pessoas": mesa.visualization.Slider("Number of people", 10, 0, 50, 1),  # Ajuste o número de pessoas
}

# Inicializando o servidor
server = mesa.visualization.ModularServer(
    ForestFire, [canvas_element, tree_chart, pie_chart], "Forest Fire", model_params
)

server.port = 8521  # Porta do servidor
server.launch()
