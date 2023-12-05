from tkinter.tix import TList
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from agent import TWare, TLagerplatz, TGabelstapler, TWarenEingang, TWarenAusgabe
from agent_routing_controller import Tagent_routing_controller

class OurModel(Model):
    def remove_agent(self, agent):
        self.grid.remove_agent(agent)
        self.schedule.remove(agent)
        self.waren_list.remove(agent)
        agent = None


    def __init__(self, number_agents_gabelstapler, number_agents_lagerplatz, number_agents_ware, width, height):
        self.agent_routing_controller: Tagent_routing_controller

        self.gabelstapler_list: list[TGabelstapler]
        self.lagerplatz_list: list[TLagerplatz]
        self.waren_list: list[TWare]

        self.num_agents_gabelstapler = number_agents_gabelstapler
        self.num_agents_lagerplatz = number_agents_lagerplatz
        self.num_agents_ware = number_agents_ware
        
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True

        self.datacollector_currents = DataCollector(
            {
                "Anzahl Gabelstapler": self.num_agents_gabelstapler,
                "Anzahl der Lagerplätze": self.num_agents_lagerplatz,
                "Anzahl der Waren": self.num_agents_ware,
            }
        )

        # Create agents
        agent_index = 0
        
        # Create TWare
        self.waren_list = []
        for i in range(agent_index, self.num_agents_ware + agent_index):
            a = TWare(agent_index, self)
            self.schedule.add(a)
            self.waren_list.append(a)

            # Add the agent to a random grid
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            agent_index= agent_index + 1

        #Create TLagerplatz
        self.lagerplatz_list = []
        for i in range(agent_index, self.num_agents_lagerplatz + agent_index):
            a = TLagerplatz(agent_index, self)
            self.schedule.add(a)
            self.lagerplatz_list.append(a)

            # Add the agent to a random grid
            x = 3 + i
            y = 10
            self.grid.place_agent(a, (x, y))
            agent_index= agent_index + 1

        gabelstapler_list = []
        #Create TGapelstapler
        for i in range(agent_index, self.num_agents_gabelstapler + agent_index):
            a = TGabelstapler(agent_index, self)
            self.schedule.add(a)
            gabelstapler_list.append(a)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            agent_index= agent_index + 1

        event_ware_aus_system_schaffen = self.remove_agent
        a = TWarenAusgabe(agent_index, self, event_ware_aus_system_schaffen)
        self.schedule.add(a)
        # Add the agent to a random grid cell
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        self.grid.place_agent(a, (x, y))
        agent_index= agent_index + 1

        self.agent_routing_controller = Tagent_routing_controller(gabelstapler_list, a)

    def step(self):
        """Advance the model by one step."""
        self.agent_routing_controller.step(self.waren_list)
        self.schedule.step()

