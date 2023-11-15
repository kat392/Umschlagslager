from mesa import Agent

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

class TGabelstapler(Agent):
    aTransportierteWare: TWare

    def __init__(self, unique_id, model):
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
            if len(other_agents):
                for agent in other_agents:
                    cells_with_agents.append(agent)

        # if there is some agent on the neighborhood
        if len(cells_with_agents) > 0:
            new_position = available_cells[0]
            # new_position = self.random.choice(available_cells)
        else:
            new_position = self.pos

        self.model.grid.move_agent(self, new_position)
