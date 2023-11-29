from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import NumberInput
from mesa.visualization.modules import CanvasGrid
from model import OurModel
from agent import TWare, TLagerplatz, TGabelstapler

NUMBER_OF_CELLS = 15

SIZE_OF_CANVAS_IN_PIXELS_X = 1000
SIZE_OF_CANVAS_IN_PIXELS_Y = 1000

simulation_params = {
    "number_agents_gabelstapler": NumberInput(
        "Anzahl der Gabelstapler", value=5
    ),
    "number_agents_lagerplatz": NumberInput(
    "Anzahl der Lagerplätze", value=5
    ),
    "number_agents_ware": NumberInput(
    "Anzahl der Waren", value=5
    ),
    "width": NUMBER_OF_CELLS,
    "height": NUMBER_OF_CELLS,
}


def agent_portrayal(agent):
    # if the agent is buried we put it as white, not showing it.
    #if agent.buried:
    if isinstance(agent, TGabelstapler):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Color": "yellow",
            "w": "1",
            "h": "1",
            "text": "Gabelstapler",
            "Layer": 1,
            "text_color": "black",
        }

    elif isinstance(agent, TWare):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Color": "blue",
            "w": "1",
            "h": "1",
            "text": "War",
            "Layer": 1,
            "text_color": "black",
        }

    elif isinstance(agent, TLagerplatz):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Color": "gray",
            "w": "1",
            "h": "1",
            "text": "Lagerplatz",
            "Layer": 1,
            "text_color": "black",
        }

    else:
        portrayal = {
           "Shape": "rect",
           "Filled": "true",
           "Color": "green",
           "w": "1",
           "h": "1",
           "text": "Default",
           "Layer": 1,
           "text_color": "black",
        }
    return portrayal


grid = CanvasGrid(
    agent_portrayal,
    NUMBER_OF_CELLS,
    NUMBER_OF_CELLS,
    SIZE_OF_CANVAS_IN_PIXELS_X,
    SIZE_OF_CANVAS_IN_PIXELS_Y,
)

# chart_currents = ChartModule(
#     [
#         {"Label": "Healthy Agents", "Color": "green"},
#         {"Label": "Non Healthy Agents", "Color": "red"},
#     ],
#     canvas_height=300,
#     data_collector_name="datacollector_currents",
# )


server = ModularServer(
    OurModel, [grid], "Lager Model", simulation_params
)
server.port = 8521  # The default
server.launch()
