from ctypes import pointer
from tkinter import Y
from turtle import pos
from mesa import Agent
from mesa.model import Model

class TWare(Agent):
    reservierer: 'TGabelstapler'

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.reservierer = None

    def step(self) -> None:
    # Procedure at each Step from Mesa
        return

class TLagerplatz(Agent):
    #aGelagerteWaren: list(TWare)

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self) -> None:
    # Procedure at each Step from Mesa
        return
    
class TWarenAusgabe(Agent):
    def __init__(self, unique_id: int, model: Model, event_ware_aus_system_schaffen) -> None:
        super().__init__(unique_id, model)
        self.event_ware_aus_system_schaffen = event_ware_aus_system_schaffen

    def ware_aus_system_schaffen(self, ware: TWare):
        if ware is not None:
            self.event_ware_aus_system_schaffen(ware)


class TWarenEingang(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)

class TGabelstapler(Agent):
    reservierte_ware: TWare
    beladene_ware: TWare
    next_way_point: pos

    def __init__(self, unique_id, model):
        self.reservierte_ware = None
        self.beladene_ware = None
        self.next_way_point = None
        super().__init__(unique_id, model)

    def entladen(self) -> TWare:
        ware = self.beladene_ware
        self.reservierte_ware = None
        self.beladene_ware = None
        ware.reservierer = None
        return ware



    def step(self) -> None:
        self.move()
        # TODO Move in verschiedene Methoden aufteilten. Waren beladung Waren entladung

    def move(self) -> None:
        available_cells = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )

        cells_with_agents = []
        # looking for agents in the cells around the agent
        for cell in available_cells:
            other_agents = self.model.grid.get_cell_list_contents([cell])
            if len(other_agents) > 0:
                for agent in other_agents:
                    cells_with_agents.append(agent)

        # if there is some agent on the neighborhood
        #if len(cells_with_agents) == 0:
        if self.next_way_point is not None:
            next_way_point_x, next_way_point_y = self.next_way_point
            current_x, current_y = self.pos

            if next_way_point_x > current_x:
                new_x = current_x + 1
            elif next_way_point_x < current_x:
                new_x = current_x - 1
            else:
                new_x = current_x

            if next_way_point_y > current_y:
                new_y = current_y + 1
            elif next_way_point_y < current_y:
                new_y = current_y - 1
            else:
                new_y = current_y

            new_position = new_x, new_y

            # besorge Zelle der neuen Position
            new_cell = self.model.grid.get_neighborhood(
                new_position, moore=False, include_center=True, radius=0
            )

            new_position_available = True
            for cell in new_cell:
                # besorge Liste der Agenten auf dem Feld
                new_cell_agents = self.model.grid.get_cell_list_contents([cell])
                # Mehr als ein Agent auf dem Feld
                if len(new_cell_agents) > 1:
                    new_position_available = False
                # Genau ein Agent auf dem Feld
                elif len(new_cell_agents) > 0:
                    new_cell_agent = new_cell_agents[0]
                    # Agent ist Ware die self reserviert hat
                    if isinstance(new_cell_agent, TWare) and new_cell_agent.reservierer == self:
                        # Lade Ware auf
                        self.beladene_ware = new_cell_agent
                    elif isinstance(new_cell_agent, TWarenAusgabe):
                        if self.beladene_ware is not None:
                            new_cell_agent.ware_aus_system_schaffen(self.entladen())
                    else:
                        new_position_available = False

            if not(new_position_available):
                new_position = self.pos
            if new_position == self.next_way_point:
                self.next_way_point = None
        else:
            new_position = self.pos

        self.model.grid.move_agent(self, new_position)
        if self.beladene_ware is not None:
            self.model.grid.move_agent(self.beladene_ware, new_position)
