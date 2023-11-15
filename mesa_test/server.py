from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import NumberInput
from mesa.visualization.modules import CanvasGrid#, ChartModule
from model import OurModel

NUMBER_OF_CELLS = 15

SIZE_OF_CANVAS_IN_PIXELS_X = 1000
SIZE_OF_CANVAS_IN_PIXELS_Y = 1000

simulation_params = {
    "number_agents": NumberInput(
        "Anzahl der Gabelstapler", value=5
    ),
    "width": NUMBER_OF_CELLS,
    "height": NUMBER_OF_CELLS,
}


def agent_portrayal(agent):
    # if the agent is buried we put it as white, not showing it.
    #if agent.buried:
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
