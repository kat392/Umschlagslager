from mesa import Agent
import math

class TWare(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

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

class TGapelstapler(Agent):
    aTransportierteWare: TWare

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self) -> None:
        self.move()
    # Procedure at each Step from Mesa
        return

    def move(self) -> None:
        """"
        available_cells = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )

        cells_with_agents = []
        # looking for agents in the cells around the agent
        for cell in available_cells:
            otherAgents = self.model.grid.get_cell_list_contents([cell])
            if len(otherAgents):
                for agent in otherAgents:
                    if not agent.dead:
                        cells_with_agents.append(agent)

        # if there is some agent on the neighborhood
        if len(cells_with_agents):
            new_position = self.random.choice(available_cells)  
        """  
        #x, y = self.pos
        #x = x + 1
        x, y = self.pos
        x = x + 1
        y = y + 2
        new_position = x, y
        self.model.grid.move_agent(self, new_position)
