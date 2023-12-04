from ctypes import pointer
from tkinter import Y
from turtle import pos
from mesa import Agent
from zmq import NULL

class TWare(Agent):
    ist_reservierer: bool

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.ist_reserviert = False

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

class TGabelstapler(Agent):
    ware: TWare
    next_way_point: pos

    def __init__(self, unique_id, model):
        self.ware = NULL
        self.next_way_point = NULL
        super().__init__(unique_id, model)

    def step(self) -> None:
        self.move()

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
        if self.next_way_point != NULL:
            next_way_point_x, next_way_point_y = self.next_way_point
            current_x, current_y = self.pos

            #if self.pos == self.ware.pos:


            if next_way_point_x > current_x:
                current_x = current_x + 1
            elif next_way_point_x < current_x:
                current_x = current_x - 1

            if next_way_point_y > current_y:
                current_y = current_y + 1
            elif next_way_point_y < current_y:
                current_y = current_y - 1

            new_position = current_x, current_y
            #self.model.grid.get
            #if new_position == self.next_way_point and self.model.grid.get_cell_list_contents([new_position])
        else:
            new_position = self.pos
            # new_position = self.random.choice(available_cells)
        #else:
        #    new_position = self.pos

        self.model.grid.move_agent(self, new_position)
