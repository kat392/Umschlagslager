from mesa import Model
from agent import TGapelstapler
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class OurModel(Model):
    def __init__(self, number_agents, width, height):
        self.num_agents = number_agents
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True

        self.datacollector_currents = DataCollector(
            {
                "Anzahl Agents": self.num_agents,
            }
        )

        # Create agents
        for i in range(self.num_agents):
            a = TGapelstapler(i, self)
            self.schedule.add(a)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))    

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
        #self.datacollector_currents.collect(self) 