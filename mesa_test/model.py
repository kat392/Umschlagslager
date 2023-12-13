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

    def create_agent(self, agent, x_pos = -1, y_pos = -1):
        self.schedule.add(agent)

        if x_pos < 0:
            x_pos = self.random.randrange(self.grid.width)
        if y_pos < 0:
            y_pos = self.random.randrange(self.grid.height)

        self.grid.place_agent(agent, (x_pos, y_pos))
        self.agent_index = self.agent_index + 1

    def create_ware(self, x_pos = -1, y_pos = -1):
        agent = TWare(self.agent_index, self)
        self.create_agent(agent, x_pos, y_pos)
        self.waren_list.append(agent)
        
    def create_lagerplatz(self, x_pos = -1, y_pos = -1):
        agent = TLagerplatz(self.agent_index, self)
        self.create_agent(agent, x_pos, y_pos)
        self.lagerplatz_list.append(agent)
        

    def __init__(self, number_agents_gabelstapler, number_agents_lagerplatz, number_agents_ware, width, height):
        self.agent_routing_controller: Tagent_routing_controller

        self.gabelstapler_list: list[TGabelstapler]
        self.lagerplatz_list: list[TLagerplatz]
        self.waren_list: list[TWare]

        self.num_agents_gabelstapler = number_agents_gabelstapler
        self.num_agents_lagerplatz = number_agents_lagerplatz
        self.num_agents_ware = number_agents_ware

        self.agent_index = 0
        
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
        # Create TWare
        self.waren_list = []
        for i in range(self.agent_index, self.num_agents_ware + self.agent_index):
            self.create_ware()

        #Create TLagerplatz
        self.lagerplatz_list = []
        for i in range(self.agent_index, self.num_agents_lagerplatz + self.agent_index):
            a = TLagerplatz(self.agent_index, self)
            self.schedule.add(a)
            self.lagerplatz_list.append(a)

            # Add the agent to a random grid
            x = 3 + i
            y = 10
            self.grid.place_agent(a, (x, y))
            self.agent_index= self.agent_index + 1

        gabelstapler_list = []
        #Create TGapelstapler
        for i in range(self.agent_index, self.num_agents_gabelstapler + self.agent_index):
            a = TGabelstapler(self.agent_index, self)
            self.schedule.add(a)
            gabelstapler_list.append(a)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            self.agent_index= self.agent_index + 1

        event_ware_in_system_schaffen = self.create_ware
        a = TWarenEingang(self.agent_index, self, event_ware_in_system_schaffen, 5)
        self.schedule.add(a)
        # Add the agent to a random grid cell
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        self.grid.place_agent(a, (x, y))
        self.agent_index= self.agent_index + 1

        event_ware_aus_system_schaffen = self.remove_agent
        a = TWarenAusgabe(self.agent_index, self, event_ware_aus_system_schaffen)
        self.schedule.add(a)
        # Add the agent to a random grid cell
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        self.grid.place_agent(a, (x, y))
        self.agent_index= self.agent_index + 1

        self.agent_routing_controller = Tagent_routing_controller(gabelstapler_list, a)

    def step(self):
        """Advance the model by one step."""
        self.agent_routing_controller.step(self.waren_list)
        self.schedule.step()
